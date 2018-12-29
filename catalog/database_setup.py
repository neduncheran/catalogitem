from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Create user table
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


# Create catalog table
class Catalog(Base):
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    item_col = relationship("CatalogItem", collection_class=set)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        items = [item.serialize for item in self.item_col]
        return {
            'name': self.name,
            'id': self.id,
            'items': items
        }


# Create catalog_Item table
class CatalogItem(Base):
    __tablename__ = 'catalog_Item'

    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(500))
    price = Column(String(8))
    category = Column(String(250))
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'category': self.category,
        }


engine = create_engine('sqlite:///sportscatalog.db')


Base.metadata.create_all(engine)
