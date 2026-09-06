from decimal import Decimal

from django.utils.text import slugify

from cocktails.models import (
    Cocktail,
    CocktailIngredient,
    Equipment,
    Glassware,
    Ingredient,
    IngredientCategory,
    Technique,
)
from learning.models import LearningPath, Lesson


def upsert(model, lookup, **defaults):
    obj, _ = model.objects.update_or_create(
        **lookup,
        defaults=defaults,
    )
    return obj


# Categorias de ingredientes

category_data = {
    "Destilados": "Bebidas alcoólicas obtidas por destilação.",
    "Licores e aperitivos": "Bebidas utilizadas para adicionar sabor, aroma e complexidade.",
    "Vinhos e espumantes": "Vinhos tranquilos, fortificados e espumantes.",
    "Frutas e sucos": "Frutas frescas e sucos utilizados na preparação de drinks.",
    "Xaropes e açúcares": "Ingredientes responsáveis principalmente pela doçura.",
    "Ervas e especiarias": "Ingredientes aromáticos utilizados no preparo e finalização.",
    "Bitters": "Preparações concentradas utilizadas para adicionar aroma e amargor.",
    "Misturadores": "Bebidas não alcoólicas utilizadas para completar drinks.",
    "Outros": "Ingredientes complementares usados em receitas.",
}

categories = {}

for name, description in category_data.items():
    categories[name] = upsert(
        IngredientCategory,
        {"slug": slugify(name)},
        name=name,
        description=description,
    )


# Ingredientes

ingredient_data = [
    ("Cachaça", "Destilados", True),
    ("Rum branco", "Destilados", True),
    ("Gin", "Destilados", True),
    ("Vodka", "Destilados", True),
    ("Tequila", "Destilados", True),
    ("Bourbon", "Destilados", True),
    ("Campari", "Licores e aperitivos", True),
    ("Aperol", "Licores e aperitivos", True),
    ("Triple sec", "Licores e aperitivos", True),
    ("Vermute rosso", "Vinhos e espumantes", True),
    ("Prosecco", "Vinhos e espumantes", True),
    ("Limão-taiti", "Frutas e sucos", False),
    ("Suco de limão-taiti", "Frutas e sucos", False),
    ("Suco de limão-siciliano", "Frutas e sucos", False),
    ("Açúcar", "Xaropes e açúcares", False),
    ("Xarope simples", "Xaropes e açúcares", False),
    ("Hortelã", "Ervas e especiarias", False),
    ("Angostura bitters", "Bitters", True),
    ("Água com gás", "Misturadores", False),
    ("Água tônica", "Misturadores", False),
    ("Ginger beer", "Misturadores", False),
    ("Clara de ovo", "Outros", False),
    ("Gelo", "Outros", False),
]

ingredients = {}

for name, category_name, is_alcoholic in ingredient_data:
    ingredients[name] = upsert(
        Ingredient,
        {"slug": slugify(name)},
        name=name,
        category=categories[category_name],
        description=f"Ingrediente utilizado no preparo de cocktails: {name}.",
        is_alcoholic=is_alcoholic,
    )


# Técnicas

technique_data = {
    "Montado": (
        "O drink é preparado diretamente no copo em que será servido.",
        "Adicione os ingredientes na ordem indicada e misture quando necessário.",
    ),
    "Batido": (
        "Os ingredientes são resfriados e misturados em uma coqueteleira.",
        "Adicione gelo e ingredientes, feche a coqueteleira e bata com firmeza.",
    ),
    "Mexido": (
        "Os ingredientes são resfriados delicadamente em um mixing glass.",
        "Misture com uma colher bailarina até atingir diluição e temperatura adequadas.",
    ),
    "Macerado": (
        "Frutas, ervas ou açúcar são pressionados para liberar aromas e sabores.",
        "Pressione suavemente para evitar amargor excessivo.",
    ),
    "Coagem simples": (
        "O drink é coado para impedir que o gelo utilizado no preparo chegue ao copo.",
        "Utilize um strainer apropriado ao tipo de coqueteleira.",
    ),
    "Coagem dupla": (
        "O drink passa por um strainer e por uma peneira fina.",
        "Use para remover pequenos fragmentos de frutas, ervas ou gelo.",
    ),
}

techniques = {}

for name, (description, instructions) in technique_data.items():
    techniques[name] = upsert(
        Technique,
        {"slug": slugify(name)},
        name=name,
        description=description,
        instructions=instructions,
    )


# Equipamentos

equipment_data = {
    "Coqueteleira": "Utilizada para bater, resfriar e diluir cocktails.",
    "Dosador": "Utilizado para medir ingredientes com precisão.",
    "Colher bailarina": "Colher longa utilizada para misturar cocktails.",
    "Macerador": "Utilizado para pressionar frutas, ervas e açúcar.",
    "Mixing glass": "Recipiente utilizado para cocktails mexidos.",
    "Strainer": "Coador utilizado para reter gelo e ingredientes sólidos.",
    "Peneira fina": "Utilizada na coagem dupla.",
    "Espremedor": "Utilizado para extrair suco de frutas cítricas.",
}

equipment = {}

for name, description in equipment_data.items():
    equipment[name] = upsert(
        Equipment,
        {"slug": slugify(name)},
        name=name,
        description=description,
    )


# Tipos de copo

glassware_data = {
    "Copo rocks": "Copo baixo utilizado para servir drinks com gelo.",
    "Copo highball": "Copo alto utilizado para drinks completados com misturadores.",
    "Taça coupe": "Taça de haste utilizada para cocktails servidos sem gelo.",
    "Taça Nick & Nora": "Taça pequena utilizada para cocktails clássicos.",
    "Taça de vinho": "Taça utilizada para vinhos e spritzes.",
    "Caneca de cobre": "Recipiente tradicionalmente associado ao Moscow Mule.",
}

glassware = {}

for name, description in glassware_data.items():
    glassware[name] = upsert(
        Glassware,
        {"slug": slugify(name)},
        name=name,
        description=description,
    )


# Cocktails

cocktail_data = [
    {
        "name": "Caipirinha",
        "description": "Clássico brasileiro preparado com cachaça, limão, açúcar e gelo.",
        "instructions": (
            "1. Corte o limão em pedaços.\n"
            "2. Coloque o limão e o açúcar no copo.\n"
            "3. Macere suavemente.\n"
            "4. Adicione a cachaça e o gelo.\n"
            "5. Misture e sirva."
        ),
        "difficulty": "easy",
        "time": 5,
        "glassware": "Copo rocks",
        "garnish": "Rodela de limão",
        "techniques": ["Macerado", "Montado"],
        "equipment": ["Dosador", "Macerador", "Colher bailarina"],
        "ingredients": [
            ("Cachaça", "60", "ml", False, 1),
            ("Limão-taiti", "1", "unit", False, 2),
            ("Açúcar", "2", "bar_spoon", False, 3),
            ("Gelo", None, "to_taste", False, 4),
        ],
    },
    {
        "name": "Mojito",
        "description": "Drink refrescante de rum, hortelã, limão e água com gás.",
        "instructions": (
            "1. Coloque hortelã e xarope no copo.\n"
            "2. Pressione levemente a hortelã.\n"
            "3. Adicione rum, limão e gelo.\n"
            "4. Complete com água com gás e misture."
        ),
        "difficulty": "medium",
        "time": 7,
        "glassware": "Copo highball",
        "garnish": "Ramo de hortelã",
        "techniques": ["Macerado", "Montado"],
        "equipment": ["Dosador", "Macerador", "Colher bailarina"],
        "ingredients": [
            ("Rum branco", "50", "ml", False, 1),
            ("Suco de limão-taiti", "25", "ml", False, 2),
            ("Xarope simples", "15", "ml", False, 3),
            ("Hortelã", "8", "unit", False, 4),
            ("Água com gás", "60", "ml", False, 5),
            ("Gelo", None, "to_taste", False, 6),
        ],
    },
    {
        "name": "Negroni",
        "description": "Cocktail italiano amargo, equilibrado e aromático.",
        "instructions": (
            "1. Adicione gin, Campari e vermute ao mixing glass com gelo.\n"
            "2. Mexa até resfriar.\n"
            "3. Coe sobre gelo novo."
        ),
        "difficulty": "medium",
        "time": 5,
        "glassware": "Copo rocks",
        "garnish": "Casca de laranja",
        "techniques": ["Mexido", "Coagem simples"],
        "equipment": ["Dosador", "Mixing glass", "Colher bailarina", "Strainer"],
        "ingredients": [
            ("Gin", "30", "ml", False, 1),
            ("Campari", "30", "ml", False, 2),
            ("Vermute rosso", "30", "ml", False, 3),
            ("Gelo", None, "to_taste", False, 4),
        ],
    },
    {
        "name": "Daiquiri",
        "description": "Cocktail cítrico e equilibrado de rum, limão e açúcar.",
        "instructions": (
            "1. Adicione os ingredientes à coqueteleira com gelo.\n"
            "2. Bata até resfriar.\n"
            "3. Faça coagem dupla para uma taça gelada."
        ),
        "difficulty": "medium",
        "time": 5,
        "glassware": "Taça coupe",
        "garnish": "",
        "techniques": ["Batido", "Coagem dupla"],
        "equipment": ["Coqueteleira", "Dosador", "Strainer", "Peneira fina"],
        "ingredients": [
            ("Rum branco", "60", "ml", False, 1),
            ("Suco de limão-taiti", "30", "ml", False, 2),
            ("Xarope simples", "20", "ml", False, 3),
        ],
    },
    {
        "name": "Margarita",
        "description": "Cocktail clássico de tequila, licor de laranja e limão.",
        "instructions": (
            "1. Adicione os ingredientes à coqueteleira com gelo.\n"
            "2. Bata até resfriar.\n"
            "3. Faça coagem dupla para uma taça gelada."
        ),
        "difficulty": "medium",
        "time": 6,
        "glassware": "Taça coupe",
        "garnish": "Borda de sal e fatia de limão",
        "techniques": ["Batido", "Coagem dupla"],
        "equipment": ["Coqueteleira", "Dosador", "Strainer", "Peneira fina"],
        "ingredients": [
            ("Tequila", "50", "ml", False, 1),
            ("Triple sec", "25", "ml", False, 2),
            ("Suco de limão-taiti", "25", "ml", False, 3),
        ],
    },
    {
        "name": "Old Fashioned",
        "description": "Cocktail clássico de whiskey, açúcar e bitters.",
        "instructions": (
            "1. Adicione os ingredientes ao copo com gelo.\ com gelo.\n"
            "2. Misture até resfriar e atingir a diluição desejada."
        ),
        "difficulty": "medium",
        "time": 5,
        "glassware": "Copo rocks",
        "garnish": "Casca de laranja",
        "techniques": ["Montado", "Mexido"],
        "equipment": ["Dosador", "Colher bailarina"],
        "ingredients": [
            ("Bourbon", "60", "ml", False, 1),
            ("Xarope simples", "10", "ml", False, 2),
            ("Angostura bitters", "2", "dash", False, 3),
            ("Gelo", None, "to_taste", False, 4),
        ],
    },
    {
        "name": "Gin Tônica",
        "description": "Drink refrescante preparado com gin e água tônica.",
        "instructions": (
            "1. Encha o copo com gelo.\n"
            "2. Adicione o gin.\n"
            "3. Complete com água tônica.\n"
            "4. Misture delicadamente."
        ),
        "difficulty": "easy",
        "time": 3,
        "glassware": "Copo highball",
        "garnish": "Fatia de limão",
        "techniques": ["Montado"],
        "equipment": ["Dosador", "Colher bailarina"],
        "ingredients": [
            ("Gin", "50", "ml", False, 1),
            ("Água tônica", "150", "ml", False, 2),
            ("Gelo", None, "to_taste", False, 3),
        ],
    },
    {
        "name": "Moscow Mule",
        "description": "Drink refrescante de vodka, limão e ginger beer.",
        "instructions": (
            "1. Encha a caneca com gelo.\n"
            "2. Adicione vodka e suco de limão.\n"
            "3. Complete com ginger beer e misture."
        ),
        "difficulty": "easy",
        "time": 4,
        "glassware": "Caneca de cobre",
        "garnish": "Fatia de limão",
        "techniques": ["Montado"],
        "equipment": ["Dosador", "Colher bailarina"],
        "ingredients": [
            ("Vodka", "50", "ml", False, 1),
            ("Suco de limão-taiti", "20", "ml", False, 2),
            ("Ginger beer", "100", "ml", False, 3),
            ("Gelo", None, "to_taste", False, 4),
        ],
    },
    {
        "name": "Whiskey Sour",
        "description": "Cocktail cítrico de whiskey, limão, açúcar e clara opcional.",
        "instructions": (
            "1. Adicione os ingredientes à coqueteleira.\n"
            "2. Caso utilize clara, bata primeiro sem gelo.\n"
            "3. Adicione gelo e bata novamente.\n"
            "4. Faça coagem dupla."
        ),
        "difficulty": "hard",
        "time": 8,
        "glassware": "Copo rocks",
        "garnish": "Angostura bitters",
        "techniques": ["Batido", "Coagem dupla"],
        "equipment": ["Coqueteleira", "Dosador", "Strainer", "Peneira fina"],
        "ingredients": [
            ("Bourbon", "60", "ml", False, 1),
            ("Suco de limão-siciliano", "30", "ml", False, 2),
            ("Xarope simples", "20", "ml", False, 3),
            ("Clara de ovo", "20", "ml", True, 4),
            ("Gelo", None, "to_taste", False, 5),
        ],
    },
    {
        "name": "Aperol Spritz",
        "description": "Aperitivo italiano leve, refrescante e levemente amargo.",
        "instructions": (
            "1. Coloque gelo na taça.\n"
            "2. Adicione prosecco e Aperol.\n"
            "3. Complete com água com gás.\n"
            "4. Misture delicadamente."
        ),
        "difficulty": "easy",
        "time": 4,
        "glassware": "Taça de vinho",
        "garnish": "Fatia de laranja",
        "techniques": ["Montado"],
        "equipment": ["Dosador", "Colher bailarina"],
        "ingredients": [
            ("Prosecco", "90", "ml", False, 1),
            ("Aperol", "60", "ml", False, 2),
            ("Água com gás", "30", "ml", False, 3),
            ("Gelo", None, "to_taste", False, 4),
        ],
    },
]

cocktails = {}

for data in cocktail_data:
    cocktail = upsert(
        Cocktail,
        {"slug": slugify(data["name"])},
        name=data["name"],
        description=data["description"],
        instructions=data["instructions"],
        difficulty=data["difficulty"],
        preparation_time=data["time"],
        glassware=glassware[data["glassware"]],
        garnish=data["garnish"],
        is_alcoholic=True,
        is_published=True,
    )

    cocktail.techniques.set(techniques[name] for name in data["techniques"])
    cocktail.equipment.set(equipment[name] for name in data["equipment"])

    valid_ingredient_ids = []

    for name, quantity, unit, optional, order in data["ingredients"]:
        ingredient = ingredients[name]
        valid_ingredient_ids.append(ingredient.pk)

        CocktailIngredient.objects.update_or_create(
            cocktail=cocktail,
            ingredient=ingredient,
            defaults={
                "quantity": Decimal(quantity) if quantity else None,
                "unit": unit,
                "is_optional": optional,
                "order": order,
            },
        )

    CocktailIngredient.objects.filter(
        cocktail=cocktail,
    ).exclude(
        ingredient_id__in=valid_ingredient_ids,
    ).delete()

    cocktails[data["name"]] = cocktail


# Trilhas e aulas

learning_data = [
    {
        "title": "Fundamentos da profissão",
        "description": ("Conhecimentos essenciais para iniciar a carreira de bartender."),
        "lessons": [
            {
                "title": "O papel do bartender",
                "summary": ("Entenda as responsabilidades de quem trabalha atrás do balcão."),
                "content": (
                    "O bartender prepara bebidas, atende clientes, organiza a "
                    "estação e ajuda a manter um ambiente seguro e acolhedor.\n\n"
                    "Além do domínio técnico, a profissão exige comunicação, "
                    "atenção, agilidade, responsabilidade e capacidade de "
                    "trabalhar em equipe."
                ),
            },
            {
                "title": "Utensílios fundamentais",
                "summary": ("Conheça as ferramentas básicas utilizadas no bar."),
                "content": (
                    "Os utensílios fundamentais incluem dosador, coqueteleira, "
                    "colher bailarina, strainer, macerador, mixing glass, "
                    "peneira fina e espremedor.\n\n"
                    "Cada equipamento possui uma função e deve ser utilizado "
                    "com segurança, limpeza e precisão."
                ),
                "equipment": [
                    "Dosador",
                    "Coqueteleira",
                    "Colher bailarina",
                    "Strainer",
                    "Macerador",
                    "Mixing glass",
                    "Peneira fina",
                    "Espremedor",
                ],
            },
            {
                "title": "Medidas e equilíbrio",
                "summary": ("Aprenda a medir e equilibrar os componentes de um cocktail."),
                "content": (
                    "A medição consistente permite reproduzir receitas e "
                    "controlar custos.\n\n"
                    "Um cocktail equilibrado combina força alcoólica, doçura, "
                    "acidez, amargor, aroma, temperatura e diluição. Use o "
                    "dosador para manter precisão."
                ),
                "cocktails": [
                    "Daiquiri",
                    "Margarita",
                    "Whiskey Sour",
                ],
                "ingredients": [
                    "Xarope simples",
                    "Suco de limão-taiti",
                    "Suco de limão-siciliano",
                ],
                "equipment": ["Dosador"],
            },
        ],
    },
    {
        "title": "Organização e mise en place",
        "description": ("Prepare sua estação para trabalhar com eficiência e consistência."),
        "lessons": [
            {
                "title": "O que é mise en place",
                "summary": ("Entenda por que a preparação acontece antes do atendimento."),
                "content": (
                    "Mise en place significa deixar ingredientes, equipamentos "
                    "e materiais preparados antes do serviço.\n\n"
                    "Uma boa preparação reduz atrasos, evita desperdícios e "
                    "permite que o bartender mantenha atenção no cliente."
                ),
            },
            {
                "title": "Organização da estação",
                "summary": ("Aprenda a posicionar equipamentos e ingredientes."),
                "content": (
                    "Os itens mais utilizados devem ficar em locais de fácil "
                    "acesso. Dosador, coqueteleira, colher bailarina, gelo e "
                    "ingredientes precisam possuir posições definidas.\n\n"
                    "Ao terminar uma tarefa, devolva cada item ao seu lugar."
                ),
                "ingredients": ["Gelo"],
                "equipment": [
                    "Dosador",
                    "Coqueteleira",
                    "Colher bailarina",
                ],
            },
            {
                "title": "Preparação para o serviço",
                "summary": ("Use uma rotina de abertura para evitar imprevistos."),
                "content": (
                    "Antes do serviço, confira gelo, frutas, sucos, xaropes, "
                    "bebidas, utensílios, copos e materiais de limpeza.\n\n"
                    "Verifique também equipamentos, validade dos produtos e "
                    "limpeza da estação."
                ),
                "ingredients": [
                    "Gelo",
                    "Limão-taiti",
                    "Suco de limão-taiti",
                    "Xarope simples",
                    "Hortelã",
                ],
                "equipment": [
                    "Dosador",
                    "Coqueteleira",
                    "Espremedor",
                    "Strainer",
                ],
            },
        ],
    },
    {
        "title": "Higiene e segurança",
        "description": ("Boas práticas para proteger clientes e profissionais."),
        "lessons": [
            {
                "title": "Higiene pessoal",
                "summary": ("Conheça os cuidados pessoais exigidos no atendimento."),
                "content": (
                    "Mãos, uniformes e utensílios devem permanecer limpos "
                    "durante todo o serviço.\n\n"
                    "Lave as mãos regularmente e evite manipular alimentos ou "
                    "gelo depois de tocar superfícies contaminadas."
                ),
                "ingredients": ["Gelo"],
            },
            {
                "title": "Manipulação de alimentos",
                "summary": ("Aprenda a armazenar e manipular ingredientes corretamente."),
                "content": (
                    "Frutas, sucos, xaropes, ervas e guarnições devem ser "
                    "armazenados em recipientes adequados, identificados e "
                    "protegidos.\n\n"
                    "Respeite os prazos de validade e o controle de temperatura."
                ),
                "ingredients": [
                    "Limão-taiti",
                    "Suco de limão-taiti",
                    "Suco de limão-siciliano",
                    "Xarope simples",
                    "Hortelã",
                    "Clara de ovo",
                ],
            },
            {
                "title": "Serviço responsável",
                "summary": ("Entenda a responsabilidade envolvida no serviço de álcool."),
                "content": (
                    "O bartender deve observar sinais de intoxicação e evitar "
                    "incentivar o consumo excessivo.\n\n"
                    "Nunca sirva bebidas alcoólicas a menores de idade e "
                    "respeite a legislação e as regras do estabelecimento."
                ),
                "ingredients": [
                    "Cachaça",
                    "Rum branco",
                    "Gin",
                    "Vodka",
                    "Tequila",
                    "Bourbon",
                ],
            },
        ],
    },
    {
        "title": "Atendimento ao cliente",
        "description": ("Desenvolva comunicação, hospitalidade e postura profissional."),
        "lessons": [
            {
                "title": "Hospitalidade no bar",
                "summary": ("Aprenda a criar uma experiência acolhedora."),
                "content": (
                    "Hospitalidade envolve atenção, respeito e disposição para "
                    "compreender o que o cliente procura.\n\n"
                    "Cumprimente, escute e mantenha comunicação clara mesmo em "
                    "períodos movimentados."
                ),
            },
            {
                "title": "Como recomendar um drink",
                "summary": ("Faça perguntas para entender as preferências do cliente."),
                "content": (
                    "Pergunte se o cliente prefere algo doce, cítrico, amargo, "
                    "forte, leve ou sem álcool.\n\n"
                    "Um Negroni possui perfil amargo; um Daiquiri é cítrico; "
                    "uma Gin Tônica é leve e refrescante. Considere possíveis "
                    "alergias e restrições."
                ),
                "cocktails": [
                    "Negroni",
                    "Daiquiri",
                    "Gin Tônica",
                ],
            },
            {
                "title": "Lidando com situações difíceis",
                "summary": ("Mantenha profissionalismo diante de conflitos."),
                "content": (
                    "Fale com calma, evite discussões e procure compreender o "
                    "problema.\n\n"
                    "Quando necessário, envolva o responsável pelo "
                    "estabelecimento ou a equipe de segurança."
                ),
            },
        ],
    },
    {
        "title": "Técnicas de preparo",
        "description": ("Aprenda os métodos essenciais para preparar cocktails."),
        "lessons": [
            {
                "title": "Cocktails montados",
                "summary": ("Aprenda a preparar drinks diretamente no copo."),
                "content": (
                    "Cocktails montados são preparados no recipiente em que "
                    "serão servidos.\n\n"
                    "A ordem dos ingredientes pode afetar mistura, apresentação "
                    "e carbonatação. Gin Tônica, Mojito e Aperol Spritz são "
                    "exemplos de drinks montados."
                ),
                "cocktails": [
                    "Gin Tônica",
                    "Mojito",
                    "Aperol Spritz",
                ],
                "techniques": ["Montado"],
                "equipment": [
                    "Dosador",
                    "Colher bailarina",
                ],
            },
            {
                "title": "Batido e coado",
                "summary": ("Entenda quando utilizar uma coqueteleira."),
                "content": (
                    "A técnica batida é adequada para receitas com sucos, "
                    "xaropes ou clara de ovo.\n\n"
                    "O movimento promove mistura, resfriamento, diluição e "
                    "aeração. Daiquiri, Margarita e Whiskey Sour usam essa "
                    "técnica."
                ),
                "cocktails": [
                    "Daiquiri",
                    "Margarita",
                    "Whiskey Sour",
                ],
                "techniques": [
                    "Batido",
                    "Coagem simples",
                    "Coagem dupla",
                ],
                "equipment": [
                    "Coqueteleira",
                    "Dosador",
                    "Strainer",
                    "Peneira fina",
                ],
            },
            {
                "title": "Cocktails mexidos",
                "summary": ("Aprenda a controlar diluição e temperatura."),
                "content": (
                    "Cocktails compostos principalmente por bebidas alcoólicas "
                    "costumam ser mexidos.\n\n"
                    "A técnica preserva uma textura limpa e reduz a incorporação "
                    "de ar. Negroni e Old Fashioned são exemplos."
                ),
                "cocktails": [
                    "Negroni",
                    "Old Fashioned",
                ],
                "techniques": [
                    "Mexido",
                    "Coagem simples",
                ],
                "equipment": [
                    "Mixing glass",
                    "Colher bailarina",
                    "Strainer",
                ],
            },
        ],
    },
    {
        "title": "Destilados e ingredientes",
        "description": ("Conheça os principais componentes utilizados no bar."),
        "lessons": [
            {
                "title": "Introdução aos destilados",
                "summary": ("Conheça as principais famílias de bebidas destiladas."),
                "content": (
                    "Cachaça, rum, gin, vodka, tequila e bourbon possuem "
                    "matérias-primas, processos e perfis sensoriais diferentes.\n\n"
                    "Conhecer essas diferenças ajuda a compreender e adaptar "
                    "receitas."
                ),
                "ingredients": [
                    "Cachaça",
                    "Rum branco",
                    "Gin",
                    "Vodka",
                    "Tequila",
                    "Bourbon",
                ],
                "cocktails": [
                    "Caipirinha",
                    "Mojito",
                    "Gin Tônica",
                    "Moscow Mule",
                    "Margarita",
                    "Old Fashioned",
                ],
            },
            {
                "title": "Doçura e acidez",
                "summary": ("Entenda como xaropes e frutas influenciam o equilíbrio."),
                "content": (
                    "A acidez oferece frescor e estrutura, enquanto o açúcar e "
                    "o xarope simples equilibram sabores agressivos.\n\n"
                    "Pequenas alterações nas proporções podem modificar "
                    "completamente o resultado."
                ),
                "ingredients": [
                    "Açúcar",
                    "Xarope simples",
                    "Limão-taiti",
                    "Suco de limão-taiti",
                    "Suco de limão-siciliano",
                ],
                "cocktails": [
                    "Caipirinha",
                    "Daiquiri",
                    "Margarita",
                    "Whiskey Sour",
                ],
            },
            {
                "title": "Bitters e modificadores",
                "summary": ("Descubra ingredientes utilizados em pequenas quantidades."),
                "content": (
                    "Angostura bitters, vermute rosso, Campari, Aperol e triple "
                    "sec adicionam aroma, amargor, doçura e complexidade.\n\n"
                    "Mesmo em pequenas quantidades, esses ingredientes podem "
                    "definir o perfil do cocktail."
                ),
                "ingredients": [
                    "Angostura bitters",
                    "Vermute rosso",
                    "Campari",
                    "Aperol",
                    "Triple sec",
                ],
                "cocktails": [
                    "Old Fashioned",
                    "Negroni",
                    "Aperol Spritz",
                    "Margarita",
                ],
            },
        ],
    },
    {
        "title": "Operação e controle do bar",
        "description": ("Aprenda noções de estoque, custo e rotina operacional."),
        "lessons": [
            {
                "title": "Controle de estoque",
                "summary": ("Registre entradas, saídas, perdas e consumo."),
                "content": (
                    "Um controle adequado permite identificar desperdícios, "
                    "prever compras e evitar falta de produtos.\n\n"
                    "Faça contagens regulares e mantenha os registros atualizados."
                ),
            },
            {
                "title": "Custo de uma receita",
                "summary": ("Entenda como calcular o custo dos ingredientes."),
                "content": (
                    "Calcule o custo proporcional de cada ingrediente e some os "
                    "valores usados na receita.\n\n"
                    "Uma Caipirinha, por exemplo, deve considerar cachaça, "
                    "limão, açúcar, gelo e guarnição."
                ),
                "cocktails": ["Caipirinha"],
                "ingredients": [
                    "Cachaça",
                    "Limão-taiti",
                    "Açúcar",
                    "Gelo",
                ],
                "equipment": ["Dosador"],
            },
            {
                "title": "Abertura e fechamento",
                "summary": ("Crie rotinas para iniciar e encerrar o serviço."),
                "content": (
                    "A abertura prepara a estação, enquanto o fechamento inclui "
                    "limpeza, armazenamento, contagem e reposição.\n\n"
                    "Checklists ajudam a manter consistência entre diferentes "
                    "turnos."
                ),
                "equipment": [
                    "Coqueteleira",
                    "Dosador",
                    "Colher bailarina",
                    "Macerador",
                    "Mixing glass",
                    "Strainer",
                    "Peneira fina",
                    "Espremedor",
                ],
            },
        ],
    },
]


def existing_items(item_map, names, item_type):
    missing = [name for name in names if name not in item_map]

    if missing:
        missing_names = ", ".join(missing)
        raise ValueError(f"{item_type} não encontrados no seed: {missing_names}")

    return [item_map[name] for name in names]


for path_order, path_data in enumerate(learning_data, start=1):
    learning_path = upsert(
        LearningPath,
        {"slug": slugify(path_data["title"])},
        title=path_data["title"],
        description=path_data["description"],
        order=path_order,
        is_published=True,
    )

    valid_lesson_ids = []

    for lesson_order, lesson_data in enumerate(
        path_data["lessons"],
        start=1,
    ):
        lesson = upsert(
            Lesson,
            {"slug": slugify(lesson_data["title"])},
            learning_path=learning_path,
            title=lesson_data["title"],
            summary=lesson_data["summary"],
            content=lesson_data["content"],
            difficulty=Lesson.Difficulty.BEGINNER,
            reading_time=5,
            order=lesson_order,
            is_published=True,
        )

        valid_lesson_ids.append(lesson.pk)

        lesson.cocktails.set(
            existing_items(
                cocktails,
                lesson_data.get("cocktails", []),
                "Cocktails",
            )
        )
        lesson.ingredients.set(
            existing_items(
                ingredients,
                lesson_data.get("ingredients", []),
                "Ingredientes",
            )
        )
        lesson.techniques.set(
            existing_items(
                techniques,
                lesson_data.get("techniques", []),
                "Técnicas",
            )
        )
        lesson.equipment.set(
            existing_items(
                equipment,
                lesson_data.get("equipment", []),
                "Equipamentos",
            )
        )

    Lesson.objects.filter(
        learning_path=learning_path,
    ).exclude(
        pk__in=valid_lesson_ids,
    ).update(is_published=False)


print("Seed concluído:")
print(f"- {Cocktail.objects.count()} cocktails")
print(f"- {Ingredient.objects.count()} ingredientes")
print(f"- {Technique.objects.count()} técnicas")
print(f"- {Equipment.objects.count()} equipamentos")
print(f"- {LearningPath.objects.count()} trilhas")
print(f"- {Lesson.objects.count()} aulas")
