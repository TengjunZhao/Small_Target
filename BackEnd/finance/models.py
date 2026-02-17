from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Family(models.Model):
    """家庭表"""
    family_name = models.CharField(max_length=50, verbose_name="家庭名称")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        verbose_name = "家庭"
        verbose_name_plural = "家庭"
        db_table = "family"

    def __str__(self):
        return self.family_name


class UserProfile(models.Model):
    """用户扩展信息（与 auth.User 一对一关联）"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='finance_profile')
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True, verbose_name="所属家庭")
    mobile = models.CharField(max_length=20, unique=True, verbose_name="手机号")
    is_admin = models.BooleanField(default=False, verbose_name="是否家庭管理员")

    class Meta:
        verbose_name = "用户财务信息"
        verbose_name_plural = "用户财务信息"
        db_table = "user_finance_profile"

    def __str__(self):
        return f"{self.user.username} 的财务信息"


# 资产负债相关Model
class Asset(models.Model):
    """资产表"""
    ASSET_TYPE_CHOICES = (
        ('liquid', '流动性资产'),
        ('investment', '投资性资产'),
        ('self_use', '自用性资产'),
    )
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name="所属家庭")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="归属人")
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES, verbose_name="资产大类")
    asset_subtype = models.CharField(max_length=50, verbose_name="资产子类")
    asset_name = models.CharField(max_length=100, verbose_name="资产名称")
    amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="金额（元）")
    yield_rate = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True, verbose_name="收益率（%）")
    purchase_time = models.DateField(null=True, blank=True, verbose_name="购置时间")
    depreciation_rate = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True, verbose_name="折旧率（%）")
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")
    remark = models.CharField(max_length=255, null=True, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "资产"
        verbose_name_plural = "资产"
        db_table = "asset"
        indexes = [
            models.Index(fields=['family', 'update_time'], name='idx_asset_family_update'),
            models.Index(fields=['asset_type'], name='idx_asset_type'),
        ]

    def __str__(self):
        return f"{self.asset_name}（{self.get_asset_type_display()}）"


class Liability(models.Model):
    """负债表"""
    LIABILITY_TYPE_CHOICES = (
        ('mortgage', '按揭类'),
        ('consumption', '消费类'),
        ('credit', '信用类'),
    )
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name="所属家庭")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="归属人")
    liability_type = models.CharField(max_length=20, choices=LIABILITY_TYPE_CHOICES, verbose_name="负债大类")
    liability_subtype = models.CharField(max_length=50, verbose_name="负债子类")
    liability_name = models.CharField(max_length=100, verbose_name="负债名称")
    principal_balance = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="本金余额（元）")
    interest_rate = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="利率（%）")
    remaining_term = models.IntegerField(null=True, blank=True, verbose_name="剩余期限（月）")
    monthly_payment = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="月供（元）")
    due_date = models.DateField(null=True, blank=True, verbose_name="还款日")
    is_overdue = models.BooleanField(default=False, verbose_name="是否逾期")
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")
    remark = models.CharField(max_length=255, null=True, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "负债"
        verbose_name_plural = "负债"
        db_table = "liability"
        indexes = [
            models.Index(fields=['family', 'update_time'], name='idx_liability_family_update'),
            models.Index(fields=['liability_type'], name='idx_liability_type'),
        ]

    def __str__(self):
        return f"{self.liability_name}（{self.get_liability_type_display()}）"


# 收支相关Model
class BudgetCategory(models.Model):
    """支出类目表"""
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name="所属家庭")
    main_category = models.CharField(max_length=100, verbose_name="主类目")
    sub_category = models.CharField(max_length=100, verbose_name="子类目")
    is_fixed = models.BooleanField(default=False, verbose_name="是否固定支出")

    class Meta:
        verbose_name = "支出类目"
        verbose_name_plural = "支出类目"
        db_table = "budget_category"
        indexes = [models.Index(fields=['family'], name='idx_budget_family')]
        unique_together = ('family', 'main_category', 'sub_category')

    def __str__(self):
        return f"{self.main_category}-{self.sub_category}"


class ExpendAlipay(models.Model):
    """支付宝账单表"""
    transaction_id = models.CharField(max_length=100, primary_key=True, verbose_name="交易ID")
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name="所属家庭")
    in_out = models.CharField(max_length=5, verbose_name="收支类型（收入/支出）")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="归属人")
    person_account = models.CharField(max_length=100, null=True, blank=True, verbose_name="支付宝账号")
    commodity = models.CharField(max_length=100, null=True, blank=True, verbose_name="商品/备注")
    exchange = models.CharField(max_length=50, null=True, blank=True, verbose_name="交易对方")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额（元）")
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name="交易状态")
    trade_category = models.CharField(max_length=50, null=True, blank=True, verbose_name="交易类目")
    tenant_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="商户ID")
    trade_time = models.DateTimeField(verbose_name="交易时间")
    budget = models.ForeignKey(BudgetCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="关联支出类目")
    remark = models.CharField(max_length=255, null=True, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "支付宝账单"
        verbose_name_plural = "支付宝账单"
        db_table = "expend_alipay"
        indexes = [models.Index(fields=['family', 'trade_time'], name='idx_alipay_family_time')]


class ExpendWechat(models.Model):
    """微信账单表"""
    transaction_id = models.CharField(max_length=100, primary_key=True, verbose_name="交易ID")
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name="所属家庭")
    trade_time = models.DateTimeField(verbose_name="交易时间")
    trade_category = models.CharField(max_length=50, null=True, blank=True, verbose_name="交易类目")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="归属人")
    commodity = models.CharField(max_length=100, null=True, blank=True, verbose_name="商品/备注")
    in_out = models.CharField(max_length=10, verbose_name="收支类型（收入/支出）")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额（元）")
    exchange = models.CharField(max_length=50, null=True, blank=True, verbose_name="交易对方")
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name="交易状态")
    tenant_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="商户ID")
    remark = models.CharField(max_length=50, null=True, blank=True, verbose_name="备注")
    budget = models.ForeignKey(BudgetCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="关联支出类目")

    class Meta:
        verbose_name = "微信账单"
        verbose_name_plural = "微信账单"
        db_table = "expend_wechat"
        indexes = [models.Index(fields=['family', 'trade_time'], name='idx_wechat_family_time')]


class ExpendMerged(models.Model):
    """合并收支表（统一查询）"""
    EXPEND_CHANNEL_CHOICES = (
        ('alipay', '支付宝'),
        ('wechat', '微信'),
        ('manual', '手动录入'),
    )
    transaction_id = models.CharField(max_length=100, primary_key=True, verbose_name="交易ID")
    expend_channel = models.CharField(max_length=10, choices=EXPEND_CHANNEL_CHOICES, verbose_name="收支渠道")
    budget = models.ForeignKey(BudgetCategory, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="支出类目")
    commodity = models.CharField(max_length=100, null=True, blank=True, verbose_name="商品/备注")
    in_out = models.CharField(max_length=5, verbose_name="收支类型（收入/支出）")
    person = models.CharField(max_length=100, null=True, blank=True, verbose_name="交易对方")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额（元）")
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name="交易状态")
    trade_time = models.DateTimeField(verbose_name="交易时间")
    belonging = models.CharField(max_length=100, null=True, blank=True, verbose_name="归属")
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name="所属家庭")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="归属人")

    class Meta:
        verbose_name = "合并收支"
        verbose_name_plural = "合并收支"
        db_table = "expend_merged"
        indexes = [
            models.Index(fields=['family', 'trade_time'], name='idx_merged_family_time'),
            models.Index(fields=['in_out'], name='idx_merged_in_out'),
        ]


class Income(models.Model):
    """收入表"""
    INCOME_TYPE_CHOICES = (
        ('active', '主动收入'),
        ('passive', '被动收入'),
    )
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name="所属家庭")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="归属人")
    income_type = models.CharField(max_length=20, choices=INCOME_TYPE_CHOICES, verbose_name="收入类型")
    income_subtype = models.CharField(max_length=50, verbose_name="收入子类")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额（元）")
    payday = models.DateField(verbose_name="到账日期")
    relate_asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="关联投资资产")
    remark = models.CharField(max_length=255, null=True, blank=True, verbose_name="备注")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        verbose_name = "收入"
        verbose_name_plural = "收入"
        db_table = "income"
        indexes = [models.Index(fields=['family', 'payday'], name='idx_income_family_payday')]


# 投资监控相关Model
class Investment(models.Model):
    """投资标的表"""
    INVEST_TYPE_CHOICES = (
        ('stock', '股票'),
        ('fund', '基金'),
        ('bond', '债券'),
        ('finance', '理财'),
        ('other', '其他'),
    )
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name="所属家庭")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name="关联资产")
    invest_type = models.CharField(max_length=20, choices=INVEST_TYPE_CHOICES, verbose_name="投资类型")
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name="标的代码")
    name = models.CharField(max_length=100, verbose_name="标的名称")
    hold_amount = models.DecimalField(max_digits=18, decimal_places=4, verbose_name="持有数量")
    cost_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="成本价")
    current_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="当前价")
    yield_rate = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True, verbose_name="累计收益率（%）")
    max_drawdown = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True, verbose_name="最大回撤（%）")
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    class Meta:
        verbose_name = "投资标的"
        verbose_name_plural = "投资标的"
        db_table = "investment"
        indexes = [models.Index(fields=['family', 'invest_type'], name='idx_invest_family_type')]


class InvestTarget(models.Model):
    """投资配置目标表"""
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name="所属家庭")
    invest_type = models.CharField(max_length=20, verbose_name="投资类型（同Investment）")
    target_ratio = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="目标占比（%）")
    tolerance_deviation = models.DecimalField(max_digits=8, decimal_places=4, default=0.05, verbose_name="容忍偏离度（默认±5%）")

    class Meta:
        verbose_name = "投资配置目标"
        verbose_name_plural = "投资配置目标"
        db_table = "invest_target"
        unique_together = ('family', 'invest_type')