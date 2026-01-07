from utils.database import get_db_connection
from model.categorymodel import CategoryCreate, CategoryUpdate

class CategoryCRUD:
    
    @staticmethod
    def create_category(category_data: CategoryCreate):
        """Insert a new category into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Categories] 
            (name, active)
            VALUES (?, ?)
            """
            cursor.execute(query, (
                category_data.name,
                category_data.active if category_data.active is not None else True
            ))
            conn.commit()
            
            # Get the inserted category_id
            cursor.execute("SELECT @@IDENTITY")
            category_id = cursor.fetchone()[0]
            
            return {"category_id": category_id, **category_data.dict()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating category: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_category(category_id: int):
        """Retrieve a single category by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT category_id, name, active FROM [dbo].[Categories] WHERE category_id = ?"
            cursor.execute(query, (category_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "category_id": row[0],
                    "name": row[1],
                    "active": row[2]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving category: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_categories():
        """Retrieve all categories"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT category_id, name, active FROM [dbo].[Categories]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            categories = []
            for row in rows:
                categories.append({
                    "category_id": row[0],
                    "name": row[1],
                    "active": row[2]
                })
            return categories
        
        except Exception as e:
            raise Exception(f"Error retrieving categories: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_category(category_id: int, category_data: CategoryUpdate):
        """Update an existing category"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if category_data.name is not None:
                update_fields.append("name = ?")
                values.append(category_data.name)
            if category_data.active is not None:
                update_fields.append("active = ?")
                values.append(category_data.active)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(category_id)
            
            query = f"UPDATE [dbo].[Categories] SET {', '.join(update_fields)} WHERE category_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Category not found")
            
            return {"message": "Category updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating category: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_category(category_id: int):
        """Delete a category"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[Categories] WHERE category_id = ?"
            cursor.execute(query, (category_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Category not found")
            
            return {"message": "Category deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting category: {str(e)}")
        finally:
            cursor.close()
            conn.close()
