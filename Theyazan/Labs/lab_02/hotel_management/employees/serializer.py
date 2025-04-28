from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'salary', 'hire_date', 'username', 'password']
        # يجب أن تكون كلمة السر مشفرة في الحياة الحقيقية، ولكن هنا نعرضها كما هي فقط لأغراض الفهم.
        extra_kwargs = {'password': {'write_only': True}}  # نعلم أن كلمة السر هي فقط للكتابة

    def create(self, validated_data):
        # إنشاء الموظف وتشفير كلمة السر
        employee = Employee(**validated_data)
        employee.set_password(validated_data['password'])  # تشفير كلمة السر
        employee.save()
        return employee

    def update(self, instance, validated_data):
        # تحديث البيانات وحفظ كلمة السر المشفرة إذا تم تعديلها
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # تشفير كلمة السر
        instance.save()
        return instance
