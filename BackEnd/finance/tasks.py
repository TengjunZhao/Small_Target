from celery import shared_task
from django.utils import timezone
from .models import UserProfile, Family, BudgetCategory, ExpendAlipay, ExpendWechat, ExpendMerged
import uuid
import logging
import os
import pandas as pd
from django.contrib.auth.models import User

# 邮件处理相关导入
import email
import imaplib
import email.header
import datetime
from zipfile import ZipFile
import shutil
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

# ========== 新增：自定义异常类（用于传递业务错误信息） ==========
class BillImportError(Exception):
    """账单导入业务异常"""
    def __init__(self, message, error_type="BusinessError"):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)

@shared_task(bind=True)
def import_bill_task(self, user_id, alipay_password='', wechat_password=''):
    """
    异步账单导入任务
    
    Args:
        user_id: 用户ID
        alipay_password: 支付宝账单密码
        wechat_password: 微信账单密码
    """
    logger.info(f"=== 开始执行账单导入任务 ===")
    logger.info(f"任务ID: {self.request.id}")
    logger.info(f"用户ID: {user_id}")
    logger.info(f"支付宝密码: {'***' if alipay_password else '无'}")
    logger.info(f"微信密码: {'***' if wechat_password else '无'}")
    
    try:
        # 获取用户信息
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
        family = user_profile.family
        
        logger.info(f"用户信息获取成功: {user.username}, 家庭: {family.family_name}")
        
        # 更新 Celery 任务状态
        self.update_state(state='PROGRESS', meta={'progress': 5, 'message': '正在获取用户配置信息'})
        
        # 获取邮箱配置
        email_username = user.email
        email_password = user_profile.mail_password
        # ========== 修改1：删除 self.update_state(FAILURE)，改为抛出自定义异常 ==========
        if not email_username:
            raise BillImportError('用户未配置邮箱信息')

        if not email_password:
            raise BillImportError('用户未配置邮箱密码')
        self.update_state(state='PROGRESS', meta={'progress': 10, 'message': '正在连接邮件服务器'})
        
        # 初始化邮件处理器
        mail_handler = MailHandler(email_username, email_password)
        if not mail_handler.login():
            raise BillImportError('邮件服务器登录失败')  # 同样抛异常
        
        self.update_state(state='PROGRESS', meta={'progress': 20, 'message': '邮件服务器连接成功，正在获取账单邮件'})
        
        # 获取邮件
        file_list = mail_handler.get_mail()
        # 测试环境
        # file_list = [r'C:\Users\Zhao Tengjun\Downloads\支付宝交易明细(20260119-20260219).zip',
        #              r'C:\Users\Zhao Tengjun\Downloads\wechat_bill_20260219_150138.zip']
        # alipay_password = '354302'
        # wechat_password = '835557'
        if not file_list:
            # 修改：不直接设置为SUCCESS，而是抛出业务异常让前台显示未找到文件
            raise BillImportError('未找到符合条件的账单邮件')
        
        self.update_state(state='PROGRESS', meta={'progress': 30, 'message': f'获取到 {len(file_list)} 个账单文件，正在处理解压密码'})
        
        # 处理解压密码
        password_dict = {}
        if alipay_password:
            password_dict['ali'] = alipay_password.encode()
        if wechat_password:
            password_dict['wechat'] = wechat_password.encode()
        self.update_state(state='PROGRESS', meta={'progress': 40, 'message': '开始处理ZIP文件'})
        
        # 处理ZIP文件
        results = []
        total_files = len(file_list)
        
        for i, file_path in enumerate(file_list):
            progress = 40 + int((i / total_files) * 40)
            
            if 'ali' in file_path or '交易' in file_path:
                if 'ali' in password_dict:
                    self.update_state(state='PROGRESS', meta={'progress': progress, 'message': f'正在处理支付宝账单: {os.path.basename(file_path)}'})
                    logger.info(f"正在处理支付宝账单: {os.path.basename(file_path)}")
                    zipfile_handler = ZipHandler(file_path, password_dict['ali'])
                    result = zipfile_handler.process_zip_file()
                    results.append(f'支付宝处理: {result}')
            elif 'wechat' in file_path or '微信' in file_path:
                if 'wechat' in password_dict:
                    self.update_state(state='PROGRESS', meta={'progress': progress, 'message': f'正在处理微信账单: {os.path.basename(file_path)}'})
                    logger.info(f"正在处理微信账单: {os.path.basename(file_path)}")
                    zipfile_handler = ZipHandler(file_path, password_dict['wechat'])
                    result = zipfile_handler.process_zip_file()
                    results.append(f'微信处理: {result}')
        
        self.update_state(state='PROGRESS', meta={'progress': 85, 'message': 'ZIP文件处理完成，正在合并数据到数据库'})
        
        # 调用数据合并逻辑
        logger.info("开始调用数据合并逻辑")
        merge_result = None
        try:
            merge_result = merge_db_data(family, user)
            logger.info("数据合并逻辑执行完成")
        except Exception as merge_error:
            logger.error(f"数据合并过程中发生错误: {str(merge_error)}")
            raise
        
        final_result = {
            'processed_files': len(file_list),
            'results': results,
            'merge_result': merge_result  # 包含合并结果信息
        }
        
        # 检查是否有合并失败记录
        merge_failed_count = 0
        if final_result.get('merge_result') and final_result['merge_result'].get('failed_count'):
            merge_failed_count = final_result['merge_result']['failed_count']
        
        # 更新任务状态，根据失败情况设置不同的消息
        if merge_failed_count > 0:
            message = f'账单导入完成，但有{merge_failed_count}条记录导入数据库失败'
        else:
            message = '账单导入成功完成'
        
        self.update_state(state='SUCCESS', meta={'progress': 100, 'message': message, 'result': final_result})
        
        logger.info(f"账单导入任务完成: {self.request.id}")
        return {'status': 'completed', 'result': final_result}
        
    except BillImportError as business_error:
        # 业务异常：更新任务状态为失败，并包含业务错误信息
        logger.warning(f"业务异常: {business_error.message}")
        logger.info(business_error)
        self.update_state(
            state='FAILURE',
            meta={
                'exc_type': business_error.error_type,
                'exc_message': business_error.message,
                'progress': 0,
                'message': business_error.message
            }
        )
        # 重新抛出异常，让 Celery 处理
        raise business_error
    except Exception as e:
        # 系统异常：收集详细信息，重新抛出
        import traceback
        import sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_details = {
            'task_id': self.request.id,
            'error_type': str(exc_type.__name__),
            'error_message': str(exc_value),
            'traceback': traceback.format_exc(),
            'user_id': user_id,
            'timestamp': timezone.now().isoformat()
        }

        logger.error(f"=== 账单导入任务严重错误 ===")
        logger.error(f"任务ID: {error_details['task_id']}")
        logger.error(f"错误类型: {error_details['error_type']}")
        logger.error(f"错误信息: {error_details['error_message']}")
        logger.error(f"用户ID: {error_details['user_id']}")
        logger.error(f"时间戳: {error_details['timestamp']}")
        logger.error(f"完整堆栈追踪:\n{error_details['traceback']}")
        logger.error("=" * 50)

        raise  # 必须重新抛出，让 Celery 处理

# 邮件处理类
class MailHandler:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.imapServ = 'imap.qq.com'
        self.imapPort = 993
        self.conn = None

    def login(self):
        try:
            logger.info(f"尝试连接邮件服务器: {self.imapServ}:{self.imapPort}")
            self.conn = imaplib.IMAP4_SSL(self.imapServ, self.imapPort)
            logger.info(f"SSL连接建立成功，尝试登录用户: {self.username}")
            self.conn.login(self.username, self.password)
            logger.info(f"邮件服务器登录成功: {self.username}")
            return True
        except imaplib.IMAP4.error as e:
            logger.error(f"IMAP协议错误: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"邮件服务器登录失败: {str(e)}")
            logger.error(f"用户名: {self.username}")
            logger.error(f"服务器: {self.imapServ}:{self.imapPort}")
            return False

    def get_mail(self):
        try:
            self.conn.select('INBOX')
            # 获取今天的邮件
            today = datetime.date.today()
            next_day = today + datetime.timedelta(days=1)
            date_range = (today.strftime("%d-%b-%Y"), next_day.strftime("%d-%b-%Y"))
            search_criteria = 'SINCE {start_date} BEFORE {end_date}'.format(
                start_date=date_range[0], end_date=date_range[1]
            )
            
            result, data = self.conn.uid('search', None, search_criteria.encode('utf-8'))
            email_ids = data[0].split()
            file_list = []
            
            for email_id in email_ids:
                result, data = self.conn.uid('fetch', email_id, '(RFC822)')
                raw_email = data[0][1]
                email_message = email.message_from_bytes(raw_email)
                decoded_subject = email.header.decode_header(email_message['Subject'])
                
                subject_parts = []
                for part in decoded_subject:
                    if isinstance(part[0], bytes):
                        decoded_text = part[0].decode(part[1] or 'utf-8', errors='ignore')
                        subject_parts.append(decoded_text)
                subject = ' '.join(subject_parts)
                logger.info(f'邮件标题: {subject}')
                
                file = None
                if '微信' in subject and '支付' in subject:
                    file = self.process_wechat_bill(email_message)
                elif '支付宝' in subject and '支付' in subject:
                    file = self.process_alipay_bill(email_message)
                
                if file:
                    file_list.append(file)
                    
            return file_list
        except Exception as e:
            logger.error(f"获取邮件失败: {str(e)}")
            return []

    def process_wechat_bill(self, email_message):
        try:
            email_content = self.get_email_content(email_message)
            download_link = self.extract_wechat_download_link(email_content)
            if download_link:
                logger.info(f'微信账单下载链接: {download_link}')
                save_path = self.download_wechat_bill(download_link)
                return save_path
            else:
                logger.warning('未找到微信账单下载链接')
                return None
        except Exception as e:
            logger.error(f"处理微信账单失败: {str(e)}")
            return None

    @staticmethod
    def process_alipay_bill(email_message):
        try:
            save_path = None
            for part in email_message.walk():
                if part.get_content_disposition() and part.get_content_disposition().startswith('attachment'):
                    encoded_filename = part.get_filename()
                    if encoded_filename:
                        decoded_filename = email.header.make_header(email.header.decode_header(encoded_filename))
                        decoded_filename = str(decoded_filename)
                        logger.info(f'附件: {decoded_filename}')

                        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                        save_path = os.path.join(downloads_folder, decoded_filename)

                        with open(save_path, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        logger.info(f'保存支付宝账单: {save_path}')
            return save_path
        except Exception as e:
            logger.error(f"处理支付宝账单失败: {str(e)}")
            return None

    @staticmethod
    def get_email_content(email_message):
        content = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/html':
                    content = part.get_payload(decode=True).decode()
                    break
        else:
            content = email_message.get_payload(decode=True).decode()
        return content

    @staticmethod
    def extract_wechat_download_link(email_content):
        try:
            email_content = email_content.replace('\n', '').replace('\r', '').replace('\t', '')
            soup = BeautifulSoup(email_content, 'html.parser')
            download_button = soup.find('a', string='                            点击下载                        ')
            if download_button:
                return download_button.get("href")
            return None
        except Exception as e:
            logger.error(f"提取微信下载链接失败: {str(e)}")
            return None

    @staticmethod
    def download_wechat_bill(download_link):
        try:
            response = requests.get(download_link, stream=True)
            if response.status_code == 200:
                current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"wechat_bill_{current_datetime}.zip"
                downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                save_path = os.path.join(downloads_folder, filename)
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                logger.info(f'保存微信账单: {save_path}')
                return save_path
            else:
                logger.error('无法下载微信账单')
                return None
        except Exception as e:
            logger.error(f"下载微信账单失败: {str(e)}")
            return None

# ZIP文件处理类
class ZipHandler:
    def __init__(self, file_path, file_password):
        self.file_path = file_path
        self.file_password = file_password
        self.tar_path = os.path.join(os.path.expanduser("~"), 'Downloads')
        self.extract_path = os.path.splitext(self.file_path)[0]

    def process_zip_file(self):
        try:
            if 'we' in self.file_path or '微信' in self.file_path:
                self.extract_zip_file()
                logger.info('微信账单处理完成')
            else:
                self.extract_zip_file()
                logger.info('支付宝账单处理完成')
            
            self.modify_csv_files()
            
            # 清理临时文件
            try:
                os.remove(self.file_path)
                shutil.rmtree(self.extract_path)
                return 'Process Success'
            except OSError as e:
                logger.warning(f"文件删除失败: {e}")
                return str(e)
        except Exception as e:
            logger.error(f"处理ZIP文件失败: {str(e)}")
            return str(e)

    def extract_zip_file(self):
        with ZipFile(self.file_path) as zip_ref:
            logger.info(f'解压文件: {self.file_path}', f'密码：{self.file_password}')
            print('解压文件:', self.file_path, '密码：', self.file_password)
            zip_ref.extractall(path=self.extract_path, pwd=self.file_password)

    def modify_csv_files(self):
        for root, dirs, files in os.walk(self.extract_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.csv'):
                    self.process_csv_file(file_path)
                elif file.endswith('.xlsx'):
                    self.process_xlsx_file(file_path)

    def process_csv_file(self, file_path):
        try:
            start_row = 0
            with open(file_path, "rb") as f:
                raw_data = f.read()
                from charset_normalizer import detect
                result = detect(raw_data)
                encoding = result["encoding"]

            with open(file_path, "r", encoding=encoding, errors="replace") as f:
                import csv
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2 and row[1]:
                        break
                    start_row += 1
            
            df = pd.read_csv(file_path, skiprows=start_row, encoding=encoding)
            self.save_to_excel(df, file_path)
        except Exception as e:
            logger.error(f"处理CSV文件失败: {str(e)}")

    def process_xlsx_file(self, file_path):
        try:
            df = pd.read_excel(file_path, skiprows=16)
            self.save_to_excel(df, file_path)
        except Exception as e:
            logger.error(f"处理XLSX文件失败: {str(e)}")

    def save_to_excel(self, df, original_path):
        try:
            if 'ali' in original_path or '交易' in original_path:
                xlsx_path = os.path.join(self.tar_path, 'ali.xlsx')
                if '金额(元)' in df.columns:
                    df['金额(元)'] = pd.to_numeric(df['金额(元)'].str.replace('¥', ''), errors='coerce')
            elif 'wechat' in original_path or '微信' in original_path:
                xlsx_path = os.path.join(self.tar_path, 'we.xlsx')
                if '金额(元)' in df.columns:
                    df['金额(元)'] = pd.to_numeric(df['金额(元)'].str.replace('¥', ''), errors='coerce')
            else:
                raise ValueError('Invalid file path')
            
            if os.path.exists(xlsx_path):
                os.remove(xlsx_path)
            
            df.to_excel(xlsx_path, index=False)
            logger.info(f'保存XLSX文件: {xlsx_path}')
        except Exception as e:
            logger.error(f"保存Excel文件失败: {str(e)}")

def merge_db_data(family, user):
    """合并数据库数据"""
    try:
        from .models import ExpendAlipay, ExpendWechat, ExpendMerged, BudgetCategory
        from django.contrib.auth.models import User
        from django.utils import timezone
        import pandas as pd
        import os
        
        # 确定文件路径
        sync_path = os.path.join(os.path.expanduser("~"), 'Downloads')
        ali_file_path = os.path.join(sync_path, 'ali.xlsx')
        we_file_path = os.path.join(sync_path, 'we.xlsx')
        logger.info(f"Family: {family}, User: {user}")
        
        # 处理支付宝数据
        if os.path.exists(ali_file_path):
            logger.info(f"开始导入支付宝数据，文件路径为：{ali_file_path}")
            import_alipay_data(ali_file_path, family, user)
            logger.info("支付宝数据导入完成")
        
        # 处理微信数据
        if os.path.exists(we_file_path):
            logger.info(f"开始导入微信数据，文件路径为：{we_file_path}")
            import_wechat_data(we_file_path, family, user)
            logger.info("微信数据导入完成")

        try:
            # 合并数据到总表
            logger.info("开始合并数据到总表")
            merge_result = merge_to_main_table(family, user)
            # logger.info(f"数据合并完成: 成功{merge_result['success_count']}条，失败{merge_result['failed_count']}条")
            # 返回合并结果，供上层函数使用
            return merge_result
        finally:
            try:
                 # 清理临时文件
                if os.path.exists(ali_file_path):
                    os.remove(ali_file_path)
                if os.path.exists(we_file_path):
                    os.remove(we_file_path)
                logger.info(f'临时文件清理完成，文件路径: {ali_file_path}, {we_file_path}')
            except OSError as e:
                logger.warning(f"清理临时文件失败: {e}")

    except Exception as e:
        logger.error(f"数据合并失败: {str(e)}")
        raise

def categorize_expense(commodity):
    """根据商品名称自动分类支出"""
    if '蚂蚁森林' in commodity:
        return '2200'
    elif '叮咚买菜' in commodity:
        return '2000'
    elif '手机充值' in commodity:
        return '1600'
    elif '停车' in commodity:
        return '1100'
    elif '外卖' in commodity:
        return '1000'
    elif '地铁' in commodity or '公交' in commodity:
        return '2401'
    else:
        return '0'

def import_alipay_data(file_path, family, user):
    """导入支付宝数据"""
    try:
        from .models import ExpendAlipay, BudgetCategory
        from django.utils import timezone
        import pandas as pd
        import datetime
        
        df = pd.read_excel(file_path)
        logger.info(f"开始导入支付宝数据，共{len(df)}条记录")
        
        for _, row in df.iterrows():
            try:
                # 提取关键字段
                transaction_id = str(row.get('交易订单号', '')).strip().replace('\t', '')[:100]
                if not transaction_id:
                    continue
                    
                trade_time = row.get('交易时间')
                if isinstance(trade_time, str):
                    trade_time = datetime.datetime.strptime(trade_time, '%Y-%m-%d %H:%M:%S')
                    # 调整时区，增加时区信息
                    trade_time = timezone.make_aware(trade_time)
                
                price = float(row.get('金额', 0))
                in_out = str(row.get('收/支', ''))[:100]
                commodity = str(row.get('商品说明', ''))[:100]
                person = str(row.get('交易对方', ''))[:100]
                exchange = str(row.get('交易对方', ''))[:50]
                status = str(row.get('交易状态', ''))[:50]
                trade_category = str(row.get('交易分类', ''))[:50]
                
                # 获取或创建预算分类
                category_id = categorize_expense(commodity)
                if category_id and category_id.isdigit():
                    # 根据ID查找或创建
                    try:
                        budget_category = BudgetCategory.objects.get(family=family, id=int(category_id))
                    except BudgetCategory.DoesNotExist:
                        # 创建新的分类
                        budget_category, _ = BudgetCategory.objects.get_or_create(
                            family=family,
                            main_category=f'自动分类-{category_id}',
                            defaults={'sub_category': '默认', 'is_fixed': False}
                        )

                # 创建或更新支付宝账单记录
                ExpendAlipay.objects.update_or_create(
                    transaction_id=transaction_id,
                    defaults={
                        'family': family,
                        'in_out': in_out,
                        'user': user,
                        'person_account': str(row.get('支付宝账户', ''))[:100],
                        'commodity': commodity,
                        'person': person,
                        'exchange': exchange,
                        'price': abs(price),
                        'status': status,
                        'trade_category': trade_category,
                        'tenant_id': str(row.get('商户订单号', ''))[:100],
                        'trade_time': trade_time,
                        'budget': budget_category,
                        'remark': str(row.get('备注', ''))[:255],
                        'user_id': user.id,
                        'family_id': family.id
                    }
                )
            except Exception as e:
                logger.warning(f"导入支付宝记录失败: {str(e)}, 数据: {row.to_dict()}")
                continue
                
    except Exception as e:
        logger.error(f"导入支付宝数据失败: {str(e)}")
        raise

def import_wechat_data(file_path, family, user):
    """导入微信数据"""
    try:
        from .models import ExpendWechat, BudgetCategory
        from django.utils import timezone
        import pandas as pd
        import datetime
        
        df = pd.read_excel(file_path)
        logger.info(f"开始导入微信数据，共{len(df)}条记录")
        
        for _, row in df.iterrows():
            try:
                # 提取关键字段
                transaction_id = str(row.get('交易单号', '')).strip().replace('\t', '')[:100]
                if not transaction_id:
                    continue
                    
                trade_time = row.get('交易时间')
                if isinstance(trade_time, str):
                    trade_time = datetime.datetime.strptime(trade_time, '%Y-%m-%d %H:%M:%S')
                    trade_time = timezone.make_aware(trade_time)
                price = float(row.get('金额(元)', 0))
                in_out = row.get('收/支')
                commodity = str(row.get('商品', ''))[:100]
                exchange = str(row.get('交易对方', ''))[:50]
                status = str(row.get('当前状态', ''))[:50]
                trade_category = str(row.get('交易类型', ''))[:50]
                person = str(row.get('交易对方', ''))[:100]
                
                # 获取或创建预算分类
                budget_category = None
                category_id = categorize_expense(commodity)
                if category_id and category_id.isdigit():
                    # 根据ID查找或创建
                    try:
                        budget_category = BudgetCategory.objects.get(family=family, id=int(category_id))
                    except BudgetCategory.DoesNotExist:
                        # 创建新的分类
                        budget_category, _ = BudgetCategory.objects.get_or_create(
                            family=family,
                            main_category=f'自动分类-{category_id}',
                            defaults={'sub_category': '默认', 'is_fixed': False}
                        )

                # 创建或更新微信账单记录
                ExpendWechat.objects.update_or_create(
                    transaction_id=transaction_id,
                    defaults={
                        'family': family,
                        'trade_time': trade_time,
                        'trade_category': trade_category,
                        'person': person,
                        'user': user,
                        'commodity': commodity,
                        'in_out': in_out,
                        'price': abs(price),
                        'exchange': exchange,
                        'status': status,
                        'tenant_id': str(row.get('商户单号', ''))[:100],
                        'remark': str(row.get('备注', ''))[:50],
                        'budget': budget_category,
                        'user_id': user.id,
                        'family_id': family.id
                    }
                )
            except Exception as e:
                logger.warning(f"导入微信记录失败: {str(e)}, 数据: {row.to_dict()}")
                continue
                
    except Exception as e:
        logger.error(f"导入微信数据失败: {str(e)}")
        raise


def merge_to_main_table(family, user):
    """合并到主收支表"""
    try:
        from .models import ExpendAlipay, ExpendWechat, ExpendMerged
        from django.contrib.auth.models import User

        # 收集失败记录
        failed_records = []
        success_count = 0

        # 获取支付宝数据 - 只获取当前用户的记录
        alipay_records = ExpendAlipay.objects.filter(family=family, user=user)
        alipay_list = []
        for record in alipay_records:
            alipay_list.append({
                'transaction_id': record.transaction_id,
                'channel': '支付宝',
                'budget_id': record.budget.id if record.budget else None,
                'commodity': record.commodity,
                'in_out': record.in_out,
                'person': record.person,
                'price': record.price,
                'status': record.status,
                'trade_time': record.trade_time,
                # 'belonging': record.belonging,
                'family_id': family.id,
                'user_id': user.id
            })

        # 获取微信数据 - 只获取当前用户的记录
        wechat_records = ExpendWechat.objects.filter(family=family, user=user)
        wechat_list = []
        for record in wechat_records:
            wechat_list.append({
                'transaction_id': record.transaction_id,
                'channel': '微信',
                'budget_id': record.budget.id if record.budget else None,
                'commodity': record.commodity,
                'in_out': record.in_out,
                'person': record.person,
                'price': record.price,
                'status': record.status,
                'trade_time': record.trade_time,
                # 'belonging': record.belonging,
                'family_id': family.id,
                'user_id': user.id
            })

        # 合并数据
        merged_data = alipay_list + wechat_list

        # 写入合并表 - 使用字典方式
        for data in merged_data:
            try:
                ExpendMerged.objects.update_or_create(
                    transaction_id=data['transaction_id'],
                    defaults={
                        'expend_channel': data['channel'].lower(),
                        'budget_id': data['budget_id'],
                        'commodity': data['commodity'][:100] if data['commodity'] is not None else "",
                        'in_out': data['in_out'][:5] if data['in_out'] is not None else "",
                        'person': data['person'][:100] if data['person'] is not None else "",
                        'price': data['price'],
                        'status': data['status'][:255] if data['status'] is not None else "",
                        'trade_time': data['trade_time'],
                        # 'belonging': data['belonging'],
                        'family_id': data['family_id'],
                        'user_id': data['user_id']
                    }
                )
                success_count += 1
            except Exception as e:
                error_info = {
                    'transaction_id': data['transaction_id'],
                    'channel': data['channel'],
                    'error': str(e),
                    'data': str(data)
                }
                failed_records.append(error_info)
                logger.warning(f"合并记录失败: {str(e)}, 数据: {data}")
                continue

        logger.info(f"数据合并完成，成功{success_count}条，失败{len(failed_records)}条")

        # 返回结果信息
        return {
            'success_count': success_count,
            'failed_count': len(failed_records),
            'failed_records': failed_records
        }

    except Exception as e:
        logger.error(f"合并到主表失败: {str(e)}")
        raise
