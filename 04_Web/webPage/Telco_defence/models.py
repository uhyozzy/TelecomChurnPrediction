from django.db import models
from .module.choice_list import sas_choice, ms_choice, ct_choice, ts_choice, sts_choice, cp_choice, cpg_choice

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

""" Work log
231017, Model Create
231019, tbUser_CLTV Add
231019, Default Add
231021-22, Choice Add
231023, New migrate
"""


# Main Schema #######################################################
class TbUser(models.Model):  # User Table, 유저 테이블
    class Meta:
        verbose_name = '유저 테이블'
        verbose_name_plural = '유저 테이블'
        managed = False
        db_table = 'tb_user'

    customer_id = models.CharField(db_column='Customer_ID', verbose_name='고객 아이디', primary_key=True, max_length=10)
    age = models.IntegerField(db_column='Age', verbose_name='나이')
    satisfaction_score = models.IntegerField(db_column='Satisfaction_Score', verbose_name='고객 관리 점수', default=1, choices=sas_choice)  # 231022, default 0 > 1로 변경, 231022, choice 추가
    membership = models.CharField(db_column='Membership', verbose_name='멤버쉽', max_length=10, blank=True, null=True, choices=ms_choice)  # 231022, choice 추가
    cltv = models.BigIntegerField(db_column='CLTV', verbose_name="고객 점수", blank=True, null=True, default=1)  # 231019, CLTV column 추가 / 231022, default 추가
    churn_value = models.IntegerField(db_column='Churn_Value', verbose_name='해지 여부', blank=True, null=True, default=0)
    changed = models.IntegerField(db_column='Changed', verbose_name='변경 여부', blank=True, null=True, default=0)
    churn_proba = models.FloatField(db_column='Churn_proba', verbose_name='해지 확률', blank=True, null=True, default=0)  # 231022, Int > Float로 변경
    churn_proba_group = models.CharField(db_column='Churn_proba_group', verbose_name='관리 그룹', max_length=10, blank=True, null=True, default='Stable', choices=cpg_choice)  # 231023, choice 추가

    def __str__(self):  # 클래스의 정보를 name으로 호출하는 함수
        return f'{self.customer_id}'


class TbContract(models.Model):  # Contract Table, 요금제 정보 테이블
    class Meta:
        verbose_name = '요금제 정보'
        verbose_name_plural = '요금제 정보'
        managed = False
        db_table = 'tb_contract'

    customer = models.OneToOneField('TbUser', models.CASCADE, db_column='Customer_ID', verbose_name='고객 아이디', primary_key=True)
    contract = models.CharField(db_column='Contract', verbose_name='계약 종류', max_length=20, blank=True, null=True, choices=ct_choice)  # 231022, choice 추가
    tenure_in_months = models.BigIntegerField(db_column='Tenure_in_months', verbose_name='계약 개월 수', blank=True, null=True, default=1)  # 231022, default 추가
    monthly_charge = models.FloatField(db_column='Monthly_Charge', verbose_name='기본 요금', blank=True, null=True)
    total_revenue = models.FloatField(db_column='Total_Revenue', verbose_name='총 요금', blank=True, null=True)

    def __str__(self):  # 클래스의 정보를 name으로 호출하는 함수
        return f'{self.customer}'


class TbService(models.Model):  # Service Table, 서비스 정보 테이블
    class Meta:
        verbose_name = '서비스 정보'
        verbose_name_plural = '서비스 정보'
        managed = False
        db_table = 'tb_service'

    customer = models.OneToOneField('TbUser', models.CASCADE, db_column='Customer_ID', verbose_name='고객 아이디', primary_key=True)
    tech_services = models.IntegerField(db_column='Tech_services', verbose_name='기술 서비스', blank=True, null=True, choices=ts_choice)  # 231022, choice 추가
    streaming_services = models.IntegerField(db_column='Streaming_services', verbose_name='부가 서비스', blank=True, null=True, choices=sts_choice)  # 231022, choice 추가
    combined_product = models.IntegerField(db_column='Combined_Product', verbose_name='결합 상품 수', blank=True, null=True, choices=cp_choice)  # 231022, choice 추가
    number_of_dependents = models.IntegerField(db_column='Number_of_Dependents', verbose_name='가족 결합 수', blank=True, null=True)

    def __str__(self):  # 클래스의 정보를 name으로 호출하는 함수
        return f'{self.customer}'
# Main Schema End #######################################################


# Log Schema #######################################################
class TbUserLog(models.Model):  # User log Table, 유저 정보 변동 저장 테이블
    class Meta:
        verbose_name = '유저 수정 로그'
        verbose_name_plural = '유저 수정 로그'
        managed = False
        db_table = 'tb_user_log'

    customer = models.ForeignKey(TbUser, models.CASCADE, db_column='Customer_ID', verbose_name='고객 아이디')
    change_time = models.DateTimeField(db_column='Change_time', verbose_name='변경 시간', auto_now_add=True)
    age = models.IntegerField(db_column='Age', verbose_name='나이')
    satisfaction_score = models.IntegerField(db_column='Satisfaction_Score', verbose_name='고객 관리 점수', default=0)
    cltv = models.BigIntegerField(db_column='CLTV', blank=True, null=True, default=0)  # 231019, CLTV column 추가 대응
    churn_value = models.IntegerField(db_column='Churn_Value', verbose_name='해지 여부', blank=True, null=True, default=0)

    def __str__(self):  # 클래스의 정보를 name으로 호출하는 함수
        return f'{self.customer}'


class TbContractLog(models.Model):  # Contract log Table, 요금제 정보 변동 저장 테이블
    class Meta:
        verbose_name = '요금제 수정 로그'
        verbose_name_plural = '요금제 수정 로그'
        managed = False
        db_table = 'tb_contract_log'

    customer = models.ForeignKey(TbContract, models.CASCADE, db_column='Customer_ID', verbose_name='고객 아이디')
    change_time = models.DateTimeField(db_column='Change_time', verbose_name='변경 시간', auto_now_add=True)
    contract = models.CharField(db_column='Contract', verbose_name='계약 종류', max_length=20, blank=True, null=True)
    tenure_in_months = models.BigIntegerField(db_column='Tenure_in_months', verbose_name='계약 개월 수', blank=True, null=True)
    monthly_charge = models.FloatField(db_column='Monthly_Charge', verbose_name='기본 요금', blank=True, null=True)
    total_revenue = models.FloatField(db_column='Total_Revenue', verbose_name='총 요금', blank=True, null=True)

    def __str__(self):  # 클래스의 정보를 name으로 호출하는 함수
        return f'{self.customer}'


class TbServiceLog(models.Model):  # Service log Table, 서비스 정보 변동 저장 테이블
    class Meta:
        verbose_name = '서비스 수정 로그'
        verbose_name_plural = '서비스 수정 로그'
        managed = False
        db_table = 'tb_service_log'

    customer = models.ForeignKey(TbService, models.CASCADE, db_column='Customer_ID', verbose_name='고객 아이디')
    change_time = models.DateTimeField(db_column='Change_time', verbose_name='변경 시간', auto_now_add=True)
    tech_services = models.IntegerField(db_column='Tech_services', verbose_name='기술 서비스', blank=True, null=True)
    streaming_services = models.IntegerField(db_column='Streaming_services', verbose_name='부가 서비스', blank=True, null=True)
    combined_product = models.IntegerField(db_column='Combined_Product', verbose_name='결합 상품 수', blank=True, null=True)
    number_of_dependents = models.IntegerField(db_column='Number_of_Dependents', verbose_name='가족 결합 수', blank=True, null=True)

    def __str__(self):  # 클래스의 정보를 name으로 호출하는 함수
        return f'{self.customer}'
# Log Schema End #######################################################


# User Statistics Schema
class TbUserAgeRange(models.Model):
    class Meta:
        verbose_name = '나이대'
        verbose_name_plural = '나이대'
        managed = False
        db_table = 'tb_user_age_range'

    under_10 = models.BigIntegerField(db_column='Under_10', blank=True, null=True)
    age_10 = models.BigIntegerField(db_column='Age_10', blank=True, null=True)
    age_20 = models.BigIntegerField(db_column='Age_20', blank=True, null=True)
    age_30 = models.BigIntegerField(db_column='Age_30', blank=True, null=True)
    age_40 = models.BigIntegerField(db_column='Age_40', blank=True, null=True)
    age_50 = models.BigIntegerField(db_column='Age_50', blank=True, null=True)
    age_60 = models.BigIntegerField(db_column='Age_60', blank=True, null=True)
    age_70 = models.BigIntegerField(db_column='Age_70', blank=True, null=True)
    age_80 = models.BigIntegerField(db_column='Age_80', blank=True, null=True)
    age_90 = models.BigIntegerField(db_column='Age_90', blank=True, null=True)


class TbUserCv(models.Model):
    class Meta:
        verbose_name = '해지 카테고리'
        verbose_name_plural = '해지 카테고리'
        managed = False
        db_table = 'tb_user_cv'

    churned = models.BigIntegerField(db_column='Churned', blank=True, null=True)
    stayed = models.BigIntegerField(db_column='Stayed', blank=True, null=True)


class TbUserSs(models.Model):
    class Meta:
        verbose_name = '관리 점수'
        verbose_name_plural = '관리 점수'
        managed = False
        db_table = 'tb_user_ss'

    ss_0 = models.BigIntegerField(db_column='SS_0', blank=True, null=True)
    ss_1 = models.BigIntegerField(db_column='SS_1', blank=True, null=True)
    ss_2 = models.BigIntegerField(db_column='SS_2', blank=True, null=True)
    ss_3 = models.BigIntegerField(db_column='SS_3', blank=True, null=True)
    ss_4 = models.BigIntegerField(db_column='SS_4', blank=True, null=True)
    ss_5 = models.BigIntegerField(db_column='SS_5', blank=True, null=True)

class TbUserCltv(models.Model):  # 231019, CTLV column 추가로 인한 통계 테이블 추가
    class Meta:
        verbose_name = '고객 점수'
        verbose_name_plural = '고객 점수'
        managed = False
        db_table = 'tb_user_cltv'

    cltv_0 = models.BigIntegerField(blank=True, null=True)
    cltv_1 = models.BigIntegerField(blank=True, null=True)
    cltv_2 = models.BigIntegerField(blank=True, null=True)
    cltv_3 = models.BigIntegerField(blank=True, null=True)
    cltv_4 = models.BigIntegerField(blank=True, null=True)
    cltv_5 = models.BigIntegerField(blank=True, null=True)
# User Statistics Schema End #######################################################


# Contract Statistics Schema #######################################################
class TbContractContract(models.Model):
    class Meta:
        verbose_name = '계약 종류'
        verbose_name_plural = '계약 종류'
        managed = False
        db_table = 'tb_contract_contract'

    m2m = models.BigIntegerField(db_column='M2M', blank=True, null=True)
    oy = models.BigIntegerField(db_column='OY', blank=True, null=True)
    ty = models.BigIntegerField(db_column='TY', blank=True, null=True)


class TbContractMonthc(models.Model):
    class Meta:
        verbose_name = '기본 요금대'
        verbose_name_plural = '기본 요금대'
        managed = False
        db_table = 'tb_contract_monthc'

    mc_20 = models.BigIntegerField(db_column='MC_20', blank=True, null=True)
    mc_30 = models.BigIntegerField(db_column='MC_30', blank=True, null=True)
    mc_40 = models.BigIntegerField(db_column='MC_40', blank=True, null=True)
    mc_50 = models.BigIntegerField(db_column='MC_50', blank=True, null=True)
    mc_60 = models.BigIntegerField(db_column='MC_60', blank=True, null=True)
    mc_70 = models.BigIntegerField(db_column='MC_70', blank=True, null=True)
    mc_80 = models.BigIntegerField(db_column='MC_80', blank=True, null=True)
    mc_90 = models.BigIntegerField(db_column='MC_90', blank=True, null=True)
    mc_100 = models.BigIntegerField(db_column='MC_100', blank=True, null=True)
    over_100 = models.BigIntegerField(db_column='Over_100', blank=True, null=True)


class TbContractTim(models.Model):
    class Meta:
        verbose_name = '계약 기간대'
        verbose_name_plural = '계약 기간대'
        managed = False
        db_table = 'tb_contract_tim'

    tim_3 = models.BigIntegerField(db_column='TiM_3', blank=True, null=True)
    tim_6 = models.BigIntegerField(db_column='TiM_6', blank=True, null=True)
    tim_12 = models.BigIntegerField(db_column='TiM_12', blank=True, null=True)
    tim_24 = models.BigIntegerField(db_column='TiM_24', blank=True, null=True)
    tim_36 = models.BigIntegerField(db_column='TiM_36', blank=True, null=True)
    tim_37 = models.BigIntegerField(db_column='TiM_37', blank=True, null=True)
# Contract Statistics Schema End #######################################################


# Service Statistics Schema #######################################################
class TbServiceCp(models.Model):
    class Meta:
        verbose_name = '결합 상품 수'
        verbose_name_plural = '결합 상품 수'
        managed = False
        db_table = 'tb_service_cp'

    cp_0 = models.BigIntegerField(db_column='CP_0', blank=True, null=True)
    cp_1 = models.BigIntegerField(db_column='CP_1', blank=True, null=True)
    cp_2 = models.BigIntegerField(db_column='CP_2', blank=True, null=True)
    cp_3 = models.BigIntegerField(db_column='CP_3', blank=True, null=True)
    cp_4 = models.BigIntegerField(db_column='CP_4', blank=True, null=True)


class TbServiceNod(models.Model):
    class Meta:
        verbose_name = '가족 결합 수'
        verbose_name_plural = '가족 결합 수'
        managed = False
        db_table = 'tb_service_nod'

    nod_0 = models.BigIntegerField(db_column='NoD_0', blank=True, null=True)
    nod_1 = models.BigIntegerField(db_column='NoD_1', blank=True, null=True)
    nod_2 = models.BigIntegerField(db_column='NoD_2', blank=True, null=True)
    nod_3 = models.BigIntegerField(db_column='NoD_3', blank=True, null=True)
    nod_4 = models.BigIntegerField(db_column='NoD_4', blank=True, null=True)
    nod_5 = models.BigIntegerField(db_column='NoD_5', blank=True, null=True)


class TbServiceSts(models.Model):
    class Meta:
        verbose_name = '부가 서비스 수'
        verbose_name_plural = '부가 서비스 수'
        managed = False
        db_table = 'tb_service_sts'

    sts_0 = models.BigIntegerField(db_column='StS_0', blank=True, null=True)
    sts_1 = models.BigIntegerField(db_column='StS_1', blank=True, null=True)
    sts_2 = models.BigIntegerField(db_column='StS_2', blank=True, null=True)


class TbServiceTs(models.Model):
    class Meta:
        verbose_name = '기술 서비스 수'
        verbose_name_plural = '기술 서비스 수'
        managed = False
        db_table = 'tb_service_ts'

    ts_0 = models.BigIntegerField(db_column='TS_0', blank=True, null=True)
    ts_1 = models.BigIntegerField(db_column='TS_1', blank=True, null=True)
    ts_2 = models.BigIntegerField(db_column='TS_2', blank=True, null=True)
    ts_3 = models.BigIntegerField(db_column='TS_3', blank=True, null=True)
    ts_4 = models.BigIntegerField(db_column='TS_4', blank=True, null=True)
# Service Statistics Schema End #######################################################