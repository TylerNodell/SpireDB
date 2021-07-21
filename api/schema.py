import graphene

from graphene_django import DjangoObjectType, DjangoListField 
from .models import Tenant 


class TenantType(DjangoObjectType): 
    class Meta:
        model = Tenant
        fields = "__all__"


class Query(graphene.ObjectType):
    all_tenants = graphene.List(TenantType)
    tenant = graphene.Field(TenantType, tenant_id=graphene.Int())

    def resolve_all_tenants(self, info, **kwargs):
        return Tenant.objects.all()

    def resolve_tenant(self, info, tenant_id):
        return Tenant.objects.get(pk=tenant_id)

class TenantInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()

class CreateTenant(graphene.Mutation):
    class Arguments:
        tenant_data = TenantInput(required=True)

    tenant = graphene.Field(TenantType)

    @staticmethod
    def mutate(root, info, tenant_data=None):
        tenant_instance = Tenant( 
            name=tenant_data.name,
        )
        tenant_instance.save()
        return CreateTenant(tenant=tenant_instance)

class UpdateTenant(graphene.Mutation):
    class Arguments:
        tenant_data = TenantInput(required=True)

    tenant = graphene.Field(TenantType)

    @staticmethod
    def mutate(root, info, tenant_data=None):

        tenant_instance = Tenant.objects.get(pk=tenant_data.id)

        if tenant_instance:
            tenant_instance.name = tenant_data.name
            tenant_instance.save()

            return UpdateTenant(tenant=tenant_instance)
        return UpdateTenant(tenant=None)

class DeleteTenant(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    tenant = graphene.Field(TenantType)

    @staticmethod
    def mutate(root, info, id):
        tenant_instance = Tenant.objects.get(pk=id)
        tenant_instance.delete()

        return None

class Mutation(graphene.ObjectType):
    create_tenant = CreateTenant.Field()
    update_tenant = UpdateTenant.Field()
    delete_tenant = DeleteTenant.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)