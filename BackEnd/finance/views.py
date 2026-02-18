import email
import os
import csv
import chardet
from charset_normalizer import detect
from zipfile import ZipFile
import pandas as pd
import imaplib
import email.header
import datetime
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup
import requests.utils
import shutil
import subprocess
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserProfile, Family, ExpendAlipay, ExpendWechat, ExpendMerged, BudgetCategory
import logging

logger = logging.getLogger(__name__)

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
            self.conn = imaplib.IMAP4_SSL(self.imapServ, self.imapPort)
            self.conn.login(self.username, self.password)
            logger.info(f"邮件服务器登录成功: {self.username}")
            return True
        except Exception as e:
            logger.error(f"邮件服务器登录失败: {str(e)}")
            return False

    def get_mail(self, mail_box='INBOX'):
        try:
            self.conn.select(mail_box)
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
        # 判断同步路径
        if not os.path.exists('E:/Sync/personal'):
            self.tar_path = 'D:/Sync/personal'
        else:
            self.tar_path = 'E:/Sync/personal'
        self.extract_path = os.path.splitext(self.file_path)[0]

    def process_zip_file(self):
        try:
            if 'we' in self.file_path or '微信' in self.file_path:
                self.extract_with_7z()
            else:
                self.extract_zip_file()
            
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
            zip_ref.extractall(path=self.extract_path, pwd=self.file_password)

    def extract_with_7z(self):
        seven_zip_path = r"C:\Program Files\7-Zip\7z.exe"
        command = [
            seven_zip_path, 'x', f'-p{self.file_password.decode()}',
            f'-o{self.extract_path}', self.file_path
        ]
        try:
            subprocess.run(command, check=True)
            logger.info("解压成功！")
        except subprocess.CalledProcessError as e:
            logger.error(f"解压失败: {e}")

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
                result = detect(raw_data)
                encoding = result["encoding"]

            with open(file_path, "r", encoding=encoding, errors="replace") as f:
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

# 账单导入API视图
class ImportBillView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # 获取请求参数
            wechat_password = request.data.get('wechat_password', '')
            alipay_password = request.data.get('alipay_password', '')
            user_id = request.data.get('user', 'user1')
            
            if not wechat_password and not alipay_password:
                return Response({
                    'code': 400,
                    'msg': '请至少提供一个账单密码',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取用户邮箱配置
            user = request.user
            family = None
            
            # 检查用户是否配置了家庭信息
            try:
                user_profile = UserProfile.objects.get(user=user)
                family = user_profile.family
            except UserProfile.DoesNotExist:
                return Response({
                    'code': 400,
                    'msg': '用户未配置家庭信息',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 使用Django内置User模型的email字段
            email_username = user.email
            email_password = request.data.get('email_password', '')  # 邮箱密码需要另外提供或存储
            
            # 检查用户是否配置了邮箱
            if not email_username:
                return Response({
                    'code': 400,
                    'msg': '用户未配置邮箱信息，请在用户资料中设置邮箱',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 初始化邮件处理器
            mail_handler = MailHandler(email_username, email_password)
            if not mail_handler.login():
                return Response({
                    'code': 500,
                    'msg': '邮件服务器登录失败',
                    'data': None
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # 获取邮件
            file_list = mail_handler.get_mail()
            if not file_list:
                return Response({
                    'code': 200,
                    'msg': '未找到符合条件的账单邮件',
                    'data': {'processed_files': 0}
                }, status=status.HTTP_200_OK)
            
            # 处理解压密码
            password_dict = {}
            if alipay_password:
                password_dict['ali'] = alipay_password.encode()
            if wechat_password:
                password_dict['wechat'] = wechat_password.encode()
            
            # 处理ZIP文件
            results = []
            for file_path in file_list:
                if 'ali' in file_path or '交易' in file_path:
                    if 'ali' in password_dict:
                        zipfile_handler = ZipHandler(file_path, password_dict['ali'])
                        result = zipfile_handler.process_zip_file()
                        results.append(f'支付宝处理: {result}')
                elif 'wechat' in file_path or '微信' in file_path:
                    if 'wechat' in password_dict:
                        zipfile_handler = ZipHandler(file_path, password_dict['wechat'])
                        result = zipfile_handler.process_zip_file()
                        results.append(f'微信处理: {result}')
            
            # 调用数据合并逻辑
            self.merge_db_data(family, user)
            
            return Response({
                'code': 200,
                'msg': '账单导入成功',
                'data': {
                    'processed_files': len(file_list),
                    'results': results
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"账单导入失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'账单导入失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def merge_db_data(self, family, user):
        """合并数据库数据，参考window.py的merge_db函数"""
        try:
            # 确定文件路径
            sync_path = 'E:/Sync/personal' if os.path.exists('E:/Sync/personal') else 'D:/Sync/personal'
            ali_file_path = os.path.join(sync_path, 'ali.xlsx')
            we_file_path = os.path.join(sync_path, 'we.xlsx')
            
            # 处理支付宝数据
            if os.path.exists(ali_file_path):
                self.import_alipay_data(ali_file_path, family, user)
            
            # 处理微信数据
            if os.path.exists(we_file_path):
                self.import_wechat_data(we_file_path, family, user)
            
            # 合并数据到总表
            self.merge_to_main_table(family)
            
            # 清理临时文件
            try:
                if os.path.exists(ali_file_path):
                    os.remove(ali_file_path)
                if os.path.exists(we_file_path):
                    os.remove(we_file_path)
            except OSError as e:
                logger.warning(f"清理临时文件失败: {e}")
                
        except Exception as e:
            logger.error(f"数据合并失败: {str(e)}")
            raise
    
    def import_alipay_data(self, file_path, family, user):
        """导入支付宝数据"""
        try:
            df = pd.read_excel(file_path)
            logger.info(f"开始导入支付宝数据，共{len(df)}条记录")
            
            for _, row in df.iterrows():
                try:
                    # 提取关键字段
                    transaction_id = str(row.get('交易号', ''))[:100]
                    if not transaction_id:
                        continue
                        
                    trade_time = row.get('交易时间')
                    if isinstance(trade_time, str):
                        trade_time = datetime.datetime.strptime(trade_time, '%Y-%m-%d %H:%M:%S')
                    
                    price = float(row.get('金额(元)', 0))
                    in_out = '支出' if price < 0 else '收入'
                    commodity = str(row.get('商品说明', ''))[:100]
                    exchange = str(row.get('交易对方', ''))[:50]
                    status = str(row.get('交易状态', ''))[:50]
                    trade_category = str(row.get('收/支', ''))[:50]
                    
                    # 获取或创建预算分类
                    budget_category = None
                    category_name = self.categorize_expense(commodity)
                    if category_name:
                        budget_category, _ = BudgetCategory.objects.get_or_create(
                            family=family,
                            main_category=category_name,
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
                            'exchange': exchange,
                            'price': abs(price),
                            'status': status,
                            'trade_category': trade_category,
                            'tenant_id': str(row.get('商户订单号', ''))[:100],
                            'trade_time': trade_time,
                            'budget': budget_category,
                            'remark': str(row.get('备注', ''))[:255]
                        }
                    )
                except Exception as e:
                    logger.warning(f"导入支付宝记录失败: {str(e)}, 数据: {row.to_dict()}")
                    continue
                    
        except Exception as e:
            logger.error(f"导入支付宝数据失败: {str(e)}")
            raise
    
    def import_wechat_data(self, file_path, family, user):
        """导入微信数据"""
        try:
            df = pd.read_excel(file_path)
            logger.info(f"开始导入微信数据，共{len(df)}条记录")
            
            for _, row in df.iterrows():
                try:
                    # 提取关键字段
                    transaction_id = str(row.get('交易单号', ''))[:100]
                    if not transaction_id:
                        continue
                        
                    trade_time = row.get('交易时间')
                    if isinstance(trade_time, str):
                        trade_time = datetime.datetime.strptime(trade_time, '%Y-%m-%d %H:%M:%S')
                    
                    price = float(row.get('金额(元)', 0))
                    in_out = '支出' if price < 0 else '收入'
                    commodity = str(row.get('商品', ''))[:100]
                    exchange = str(row.get('交易对方', ''))[:50]
                    status = str(row.get('当前状态', ''))[:50]
                    trade_category = str(row.get('交易类型', ''))[:50]
                    
                    # 获取或创建预算分类
                    budget_category = None
                    category_name = self.categorize_expense(commodity)
                    if category_name:
                        budget_category, _ = BudgetCategory.objects.get_or_create(
                            family=family,
                            main_category=category_name,
                            defaults={'sub_category': '默认', 'is_fixed': False}
                        )
                    
                    # 创建或更新微信账单记录
                    ExpendWechat.objects.update_or_create(
                        transaction_id=transaction_id,
                        defaults={
                            'family': family,
                            'trade_time': trade_time,
                            'trade_category': trade_category,
                            'user': user,
                            'commodity': commodity,
                            'in_out': in_out,
                            'price': abs(price),
                            'exchange': exchange,
                            'status': status,
                            'tenant_id': str(row.get('商户单号', ''))[:100],
                            'remark': str(row.get('备注', ''))[:50],
                            'budget': budget_category
                        }
                    )
                except Exception as e:
                    logger.warning(f"导入微信记录失败: {str(e)}, 数据: {row.to_dict()}")
                    continue
                    
        except Exception as e:
            logger.error(f"导入微信数据失败: {str(e)}")
            raise
    
    def merge_to_main_table(self, family):
        """合并到主收支表"""
        try:
            # 获取支付宝数据
            alipay_records = ExpendAlipay.objects.filter(family=family)
            alipay_list = []
            for record in alipay_records:
                alipay_list.append([
                    record.transaction_id,
                    '支付宝',
                    record.budget.id if record.budget else None,
                    record.commodity,
                    record.in_out,
                    record.user.username if record.user else '',
                    record.price,
                    record.status,
                    record.trade_time,
                    '户主'  # TODO: 根据实际业务逻辑确定归属
                ])
            
            # 获取微信数据
            wechat_records = ExpendWechat.objects.filter(family=family)
            wechat_list = []
            for record in wechat_records:
                wechat_list.append([
                    record.transaction_id,
                    '微信',
                    record.budget.id if record.budget else None,
                    record.commodity,
                    record.in_out,
                    record.user.username if record.user else '',
                    record.price,
                    record.status,
                    record.trade_time,
                    '户主'  # TODO: 根据实际业务逻辑确定归属
                ])
            
            # 合并数据
            merged_data = alipay_list + wechat_list
            
            # 写入合并表
            for data in merged_data:
                try:
                    ExpendMerged.objects.update_or_create(
                        transaction_id=data[0],
                        defaults={
                            'family': family,
                            'expend_channel': data[1].lower(),
                            'budget_id': data[2],
                            'commodity': data[3][:100],
                            'in_out': data[4][:5],
                            'user': User.objects.get(username=data[5]) if data[5] else None,
                            'price': data[6],
                            'status': data[7][:255],
                            'trade_time': data[8],
                        }
                    )
                except Exception as e:
                    logger.warning(f"合并记录失败: {str(e)}, 数据: {data}")
                    continue
                    
            logger.info(f"数据合并完成，共处理{len(merged_data)}条记录")
            
        except Exception as e:
            logger.error(f"合并到主表失败: {str(e)}")
            raise
    
    def categorize_expense(self, commodity):
        """根据商品名称自动分类支出"""
        if '蚂蚁森林' in commodity:
            return '环保公益'
        elif '叮咚买菜' in commodity or '超市' in commodity or '生鲜' in commodity:
            return '食品酒水'
        elif '手机充值' in commodity:
            return '通讯物流'
        elif '停车' in commodity:
            return '汽车交通'
        elif '外卖' in commodity:
            return '食品酒水'
        elif '地铁' in commodity or '公交' in commodity or '打车' in commodity:
            return '汽车交通'
        elif '电费' in commodity or '水费' in commodity or '燃气' in commodity:
            return '住房缴费'
        elif '房租' in commodity:
            return '住房缴费'
        elif '电影' in commodity or '娱乐' in commodity:
            return '休闲娱乐'
        elif '购物' in commodity or '商城' in commodity:
            return '购物消费'
        else:
            return '其他支出'

# 待确认支出明细API视图
class PendingExpenseListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print("PendingExpenseListView GET method called")  # 调试信息
        print(f"Request user authenticated: {request.user.is_authenticated}")
        print(f"Request user: {request.user}")
        print(f"Request user id: {getattr(request.user, 'id', 'No ID')}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request META: {dict(request.META)}")
        """获取待确认支出明细（belonging字段为空的记录）"""
        try:
            # 获取分页参数
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            offset = (page - 1) * page_size
            
            # 获取当前用户的家庭信息
            user = request.user
            print(f"DEBUG: Current user: {user.username if user.is_authenticated else 'Anonymous'}")
            try:
                user_profile = UserProfile.objects.get(user=user)
                family = user_profile.family
                print(f"DEBUG: User profile family: {family.family_name if family else 'None'}")
            except UserProfile.DoesNotExist:
                print("DEBUG: UserProfile.DoesNotExist")
                return Response({
                    'code': 400,
                    'msg': '用户未配置家庭信息',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 查询belonging字段为空的记录，按trade_time倒序排列
            queryset = ExpendMerged.objects.filter(
                family=family,
                belonging__isnull=True
            ).select_related('budget').order_by('-trade_time')
            
            # 获取总数
            total_count = queryset.count()
            
            # 分页查询
            records = queryset[offset:offset + page_size]
            
            # 获取所有预算子分类选项
            budget_sub_categories = list(BudgetCategory.objects.filter(
                family=family
            ).values_list('sub_category', flat=True).distinct())
            
            # 序列化数据
            data_list = []
            for record in records:
                data_list.append({
                    'transaction_id': record.transaction_id,
                    'time': record.trade_time.strftime('%Y-%m-%d %H:%M:%S') if record.trade_time else '',
                    'amount': float(record.price) if record.price else 0,
                    'in_out': record.in_out or '',
                    'commodity': record.commodity or '',
                    'main_category': record.budget.main_category if record.budget else '',
                    'sub_category': record.budget.sub_category if record.budget else '',
                    'belonging': record.belonging or '',
                    'person': record.person or '',
                    'expend_channel': record.get_expend_channel_display() or record.expend_channel
                })
            
            return Response({
                'code': 200,
                'msg': '获取待确认支出明细成功',
                'data': {
                    'records': data_list,
                    'budget_sub_categories': budget_sub_categories,
                    'total': total_count,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': (total_count + page_size - 1) // page_size
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"获取待确认支出明细失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'获取待确认支出明细失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """确认支出记录（更新belonging字段）"""
        try:
            record_id = request.data.get('transaction_id')
            category = request.data.get('category')
            belonging = request.data.get('belonging')  # 默认归属为户主
            adjusted_sub_category = request.data.get('adjusted_sub_category', '')
            print(f"DEBUG: Record ID: {record_id}, {category} ,{belonging}, {adjusted_sub_category}")
            if not record_id:
                return Response({
                    'code': 400,
                    'msg': '记录ID不能为空',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 查找记录
            try:
                record = ExpendMerged.objects.get(transaction_id=record_id)
            except ExpendMerged.DoesNotExist:
                return Response({
                    'code': 404,
                    'msg': '记录不存在',
                    'data': None
                }, status=status.HTTP_404_NOT_FOUND)
            
            # 更新记录
            record.belonging = belonging
            if belonging:
                record.status = belonging
            record.save()
            
            # 如果提供了调整的子分类，查找对应的预算分类
            if adjusted_sub_category:
                try:
                    # 根据调整的子分类查找budget_category
                    budget_category = BudgetCategory.objects.get(
                        family=record.family,
                        sub_category=adjusted_sub_category
                    )
                    record.budget = budget_category
                    record.save()
                    logger.info(f"更新预算分类成功: {budget_category.main_category} - {budget_category.sub_category}")
                except BudgetCategory.DoesNotExist:
                    # 如果找不到对应的预算分类，创建一个新的
                    if category:
                        budget_category, created = BudgetCategory.objects.get_or_create(
                            family=record.family,
                            main_category=category,
                            defaults={'sub_category': adjusted_sub_category, 'is_fixed': False}
                        )
                        record.budget = budget_category
                        record.save()
                        logger.info(f"创建新的预算分类: {budget_category.main_category} - {budget_category.sub_category}")
                    else:
                        logger.warning("未提供主分类，无法创建预算分类")
                except Exception as e:
                    logger.error(f"更新预算分类失败: {str(e)}")
            # 如果只提供了主分类但没有调整子分类
            elif category and not record.budget:
                try:
                    budget_category, created = BudgetCategory.objects.get_or_create(
                        family=record.family,
                        main_category=category,
                        defaults={'sub_category': '默认', 'is_fixed': False}
                    )
                    record.budget = budget_category
                    record.save()
                except Exception as e:
                    logger.warning(f"更新预算分类失败: {str(e)}")
            
            return Response({
                'code': 200,
                'msg': '支出记录确认成功',
                'data': {
                    'transaction_id': record.transaction_id,
                    'belonging': record.belonging
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"确认支出记录失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'确认支出记录失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 家庭成员列表API视图
class FamilyMembersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取当前用户所属家庭的所有成员"""
        try:
            user = request.user
            print(f"获取家庭成员列表，当前用户: {user.username}")
            
            # 获取当前用户的家庭信息
            try:
                user_profile = UserProfile.objects.get(user=user)
                family = user_profile.family
                print(f"用户家庭: {family.family_name if family else 'None'}")
            except UserProfile.DoesNotExist:
                return Response({
                    'code': 400,
                    'msg': '用户未配置家庭信息',
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not family:
                return Response({
                    'code': 400,
                    'msg': '用户未分配到任何家庭',
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取同一家庭的所有用户
            family_members = UserProfile.objects.filter(family=family).select_related('user')
            
            # 构造返回数据
            members_list = []
            for member_profile in family_members:
                members_list.append({
                    'user_id': member_profile.user.id,
                    'username': member_profile.user.username,
                    'is_admin': member_profile.is_admin,
                    'mobile': member_profile.mobile
                })
            
            print(f"找到 {len(members_list)} 个家庭成员")
            
            return Response({
                'code': 200,
                'msg': '获取家庭成员成功',
                'data': members_list
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"获取家庭成员列表失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'获取家庭成员失败: {str(e)}',
                'data': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 用户邮箱配置API视图
class UserEmailConfigView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 获取用户邮箱配置
        try:
            user = request.user
            email = user.email or ''
            
            return Response({
                'code': 200,
                'msg': '获取邮箱配置成功',
                'data': {
                    'email': email,
                    'configured': bool(email)
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"获取邮箱配置失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'获取邮箱配置失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        # 设置用户邮箱配置
        try:
            email = request.data.get('email')
            email_password = request.data.get('email_password', '')
            
            if not email:
                return Response({
                    'code': 400,
                    'msg': '邮箱不能为空',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = request.user
            
            # 更新Django内置User模型的email字段
            user.email = email
            user.save()
            
            # 注意：出于安全考虑，邮箱密码不应该明文存储
            # 如果需要存储邮箱密码，应该使用加密方式存储
            # 这里暂时不处理邮箱密码存储
            
            return Response({
                'code': 200,
                'msg': '邮箱配置保存成功',
                'data': {
                    'email': email,
                    'configured': True
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"保存邮箱配置失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'保存邮箱配置失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 收支明细API视图
class BillListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("BillListView GET method called")  # 调试信息
        print(f"Request user authenticated: {request.user.is_authenticated}")
        print(f"Request user: {request.user}")
        print(f"Request user id: {getattr(request.user, 'id', 'No ID')}")
        try:
            # 获取当前用户的家庭信息
            user = request.user
            try:
                user_profile = UserProfile.objects.get(user=user)
                family = user_profile.family
            except UserProfile.DoesNotExist:
                return Response({
                    'code': 400,
                    'msg': '用户未配置家庭信息',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST)

            # 1. 获取前端传入的参数（带默认值，避免KeyError）
            try:
                page = int(request.GET.get('page', 1))
                page_size = int(request.GET.get('page_size', 10))
                print(f"分页参数: page={page}, page_size={page_size}")
            except (ValueError, TypeError) as e:
                logger.error(f"分页参数转换错误: {str(e)}, GET参数: {dict(request.GET)}")
                return Response({
                    'code': 400,
                    'msg': '分页参数格式错误',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST)
            print(page, page_size)
            user_id = request.GET.get('user_id', '')  # 用户ID筛选
            category_id = request.GET.get('category_id', '')  # 分类ID筛选
            start_date = request.GET.get('startDate', '')
            end_date = request.GET.get('endDate', '')
            print(user_id, category_id, start_date, end_date)
            # 2. 初始化查询集（基础查询：当前家庭的所有支出记录）
            queryset = ExpendMerged.objects.filter(family=family)
            print(f"初始查询集数量: {queryset.count()}")
            
            # 3. 条件过滤：只在参数有值时才添加过滤条件
            # 过滤用户（如果传了user_id）
            if user_id and user_id.strip():
                queryset = queryset.filter(user_id=user_id)

            # 过滤分类（如果传了category_id）
            if category_id and category_id.strip():
                queryset = queryset.filter(budget_id=category_id)

            # 过滤时间范围（开始时间）
            if start_date and start_date.strip():
                try:
                    # 解析前端传入的日期字符串（格式：YYYY-MM-DD）
                    start_datetime = dt.strptime(start_date, '%Y-%m-%d')
                    queryset = queryset.filter(trade_time__gte=start_datetime)
                except ValueError:
                    return Response({
                        'code': 400,
                        'msg': '开始日期格式错误，请使用YYYY-MM-DD格式',
                        'data': {}
                    })

            # 过滤时间范围（结束时间）
            if end_date and end_date.strip():
                try:
                    end_datetime = dt.strptime(end_date, '%Y-%m-%d')
                    # 结束时间加一天，确保包含当天所有记录
                    end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
                    queryset = queryset.filter(trade_time__lte=end_datetime)
                except ValueError:
                    return Response({
                        'code': 400,
                        'msg': '结束日期格式错误，请使用YYYY-MM-DD格式',
                        'data': {}
                    })

            # 4. 分页处理
            total = queryset.count()  # 总记录数
            # 计算偏移量（page从1开始）
            offset = (page - 1) * page_size
            # 分页查询
            records = queryset.order_by('-trade_time')[offset:offset + page_size]

            # 5. 序列化数据
            data_list = []
            for record in records:
                data_list.append({
                    'transaction_id': record.transaction_id,
                    'time': record.trade_time.strftime('%Y-%m-%d %H:%M:%S') if record.trade_time else '',
                    'amount': float(record.price) if record.price else 0,
                    'merchant': record.person or '',
                    'commodity': record.commodity or '',
                    'category': record.budget.sub_category if record.budget else '',
                    'user': record.user.username if record.user else '',
                    'remark': record.status or '',
                    'belonging': record.belonging or ''
                })

            # 6. 获取预算分类列表（包含ID和子分类名称）
            budget_categories = list(BudgetCategory.objects.filter(
                family=family
            ).values('id', 'sub_category').distinct())

            # 7. 构造返回数据（匹配前端预期格式）
            return Response({
                'code': 200,
                'msg': '查询成功',
                'data': {
                    'records': data_list,
                    'page': page,
                    'page_size': page_size,
                    'total': total,
                    'total_pages': (total + page_size - 1) // page_size,  # 总页数
                    'budget_categories': budget_categories
                }
            })

        except Exception as e:
            logger.error(f"查询收支明细失败: {str(e)}")
            # 异常捕获，返回友好提示
            return Response({
                'code': 500,
                'msg': f'查询失败：{str(e)}',
                'data': {}
            })