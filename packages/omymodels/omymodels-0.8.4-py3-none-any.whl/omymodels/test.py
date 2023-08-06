from omymodels import create_models


models_from = """

CREATE TYPE "material_type" AS ENUM (
  'video',
  'article'
);

CREATE TABLE "material" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar NOT NULL,
  "description" text,
  "link" varchar NOT NULL,
  "type" material_type,
  "additional_properties" json,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp
);
"""

result = create_models(ddl=models_from)["code"]
print(result)
