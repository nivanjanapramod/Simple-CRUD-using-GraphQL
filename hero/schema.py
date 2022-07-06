import graphene
from graphene_django import DjangoObjectType

from .models import Hero

class HeroType(DjangoObjectType):
    class Meta:
        model = Hero


class Query(graphene.ObjectType):
    all_heroes = graphene.List(HeroType)
    heroes = graphene.Field(HeroType, id=graphene.ID())

    def resolve_all_heroes(self, info, **kwargs):
        return Hero.objects.all()

    def resolve_heroes(self, info, id):
        return Hero.objects.get(pk=id)


## Mutations

class CreateHero(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        gender = graphene.String()
        movie = graphene.String()

    hero = graphene.Field(HeroType)

    def mutate(self, info, name, gender=None, movie=None):
        hero = Hero.objects.create(
            name = name,
            gender = gender,
            movie = movie
            )
    
        hero.save()
        return CreateHero(
            hero=hero
        )



class UpdateHero(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        gender = graphene.String()
        movie = graphene.String()

    hero = graphene.Field(HeroType)

    def mutate(self, info, id, name=None, gender=None, movie=None):
        hero = Hero.objects.get(pk=id)
        hero.name = name if name is not None else hero.name
        hero.gender = gender if gender is not None else hero.gender
        hero.movie = movie if movie is not None else hero.movie
    
        hero.save()
        return UpdateHero(
            hero=hero
        )

class DeleteHero(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    hero = graphene.Field(HeroType)

    def mutate(seld, info, id):
        hero = Hero.objects.get(pk=id)

        if hero is not None:
            hero.delete()
            return DeleteHero(hero=hero)


class Mutation(graphene.ObjectType):
  create_hero = CreateHero.Field()
  update_hero = UpdateHero.Field()
  delete_hero = DeleteHero.Field()