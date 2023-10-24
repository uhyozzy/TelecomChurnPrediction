""" Choice need column
    satisfaction_score = models.IntegerField(db_column='Satisfaction_Score', verbose_name='고객 관리 점수', default=1)
    membership = models.CharField(db_column='Membership', verbose_name='멤버쉽', max_length=10, blank=True, null=True)
    contract = models.CharField(db_column='Contract', verbose_name='계약 종류', max_length=20, blank=True, null=True)
    tech_services = models.IntegerField(db_column='Tech_services', verbose_name='기술 서비스', blank=True, null=True)
    streaming_services = models.IntegerField(db_column='Streaming_services', verbose_name='부가 서비스', blank=True, null=True)
    combined_product = models.IntegerField(db_column='Combined_Product', verbose_name='결합 상품 수', blank=True, null=True)
"""
# (model, display)

sas_choice = (  # Satisfaction_score
    (1, '1점'),
    (2, '2점'),
    (3, '3점'),
    (4, '4점'),
    (5, '5점'),
)

ms_choice = (  # Membership
    ("None", '없음'),
    ("Offer A", 'A tier'),
    ("Offer B", 'B tier'),
    ("Offer C", 'C tier'),
    ("Offer D", 'D tier'),
    ("Offer E", 'E tier'),

)

ct_choice = (  # Contract 
    ("Month-to-Month", "무약정"),
    ("One Year", "1년 약정"),
    ("Two Year", "2년 약정"),
)

ts_choice = (  # Tech_services
    (0, '0개'),
    (1, '1개'),
    (2, '2개'),
    (3, '3개'),
    (4, '4개'),
)

sts_choice = (  # Streamin_services
    (0, '0개'),
    (1, '1개'),
    (2, '2개'),
)

cp_choice = (  # Combined_product
    (1, '1개'),
    (2, '2개'),
    (3, '3개'),
    (4, '4개'),
)

cpg_choice = (  # Combined_product
    ('Stable', '안정 그룹'),
    ('Potential', '잠재적 그룹'),
    ('High', '고위험 그룹'),
)