from pydantic import BaseModel, ConfigDict


class ImageCategoryBase(BaseModel):
    category_name: str
    image_url: str


class ImageCategoryCreate(ImageCategoryBase):
    pass


class ImageCategoryResponse(ImageCategoryBase):
    model_config = ConfigDict(from_attributes=True)
