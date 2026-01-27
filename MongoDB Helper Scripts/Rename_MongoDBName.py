from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import sys

# MongoDB connection details
MONGO_HOST = "10.0.138.165"
MONGO_PORT = 27017

# Database names
SOURCE_DB = "Israel_Patents_Lens"  
TARGET_DB = "Patent_Lens_Israel"  

def copy_collection(source_collection, target_collection):
    """Helper function to copy a single collection with its data and indexes."""
    # Get all documents from source collection
    documents = list(source_collection.find())
    
    if documents:
        # Insert documents into target collection
        target_collection.insert_many(documents)
    
    # Copy indexes
    indexes = list(source_collection.list_indexes())
    for index in indexes:
        if index['name'] != '_id_':  # Skip default _id index
            try:
                target_collection.create_index(
                    [(key, direction) for key, direction in index['key'].items()],
                    name=index['name'],
                    unique=index.get('unique', False)
                )
            except Exception as e:
                print(f"    Warning: Could not copy index {index['name']}: {e}")
    
    return len(documents)

def rename_database(source_db_name, target_db_name, drop_source=True):
    """
    Rename a MongoDB database by copying all collections to a new database.
    Uses a temporary database as mediator if case-insensitive conflict exists.
    
    Args:
        source_db_name: Name of the source database
        target_db_name: Name of the target database
        drop_source: Whether to drop the source database after copying (default: False)
    """
    try:
        # Connect to MongoDB
        client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/", serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print(f"✓ Connected to MongoDB at {MONGO_HOST}:{MONGO_PORT}")
        
        # Check if source database exists
        if source_db_name not in client.list_database_names():
            print(f"✗ Source database '{source_db_name}' does not exist!")
            return False
        
        # Check for case-insensitive name conflict
        db_names_lower = {name.lower(): name for name in client.list_database_names()}
        has_case_conflict = (
            source_db_name.lower() == target_db_name.lower() and 
            source_db_name != target_db_name
        )
        
        if has_case_conflict:
            print(f"⚠ Detected case-only rename: '{source_db_name}' → '{target_db_name}'")
            print(f"  Using temporary database as mediator to avoid MongoDB case conflict...")
            
            # Use temp database as mediator
            temp_db_name = f"{target_db_name}_TEMP_{int(__import__('time').time())}"
            
            # Step 1: Copy source to temp
            print(f"\n[Step 1/3] Copying '{source_db_name}' → '{temp_db_name}'")
            source_db = client[source_db_name]
            temp_db = client[temp_db_name]
            collections = source_db.list_collection_names()
            print(f"  Found {len(collections)} collections")
            
            for collection_name in collections:
                print(f"    Copying collection: {collection_name}...", end=" ")
                doc_count = copy_collection(source_db[collection_name], temp_db[collection_name])
                print(f"✓ ({doc_count} documents)")
            
            # Step 2: Drop source
            print(f"\n[Step 2/3] Dropping original database '{source_db_name}'")
            client.drop_database(source_db_name)
            print(f"  ✓ Dropped '{source_db_name}'")
            
            # Step 3: Copy temp to target
            print(f"\n[Step 3/3] Copying '{temp_db_name}' → '{target_db_name}'")
            target_db = client[target_db_name]
            collections = temp_db.list_collection_names()
            
            for collection_name in collections:
                print(f"    Copying collection: {collection_name}...", end=" ")
                doc_count = copy_collection(temp_db[collection_name], target_db[collection_name])
                print(f"✓ ({doc_count} documents)")
            
            # Drop temp database
            print(f"\n  Cleaning up temporary database '{temp_db_name}'...")
            client.drop_database(temp_db_name)
            print(f"  ✓ Dropped temporary database")
            
            print(f"\n✓ Successfully renamed '{source_db_name}' to '{target_db_name}' (via temp)")
            return True
        
        # Normal case (no case conflict)
        source_db = client[source_db_name]
        target_db = client[target_db_name]
        
        # Check if target database already exists
        if target_db_name in client.list_database_names():
            response = input(f"⚠ Target database '{target_db_name}' already exists. Overwrite? (yes/no): ")
            if response.lower() != 'yes':
                print("Operation cancelled.")
                return False
        
        # Get all collections from source database
        collections = source_db.list_collection_names()
        print(f"\nFound {len(collections)} collections in '{source_db_name}'")
        
        # Copy each collection
        for collection_name in collections:
            print(f"  Copying collection: {collection_name}...", end=" ")
            doc_count = copy_collection(source_db[collection_name], target_db[collection_name])
            print(f"✓ ({doc_count} documents)")
        
        print(f"\n✓ Successfully copied all collections from '{source_db_name}' to '{target_db_name}'")
        
        # Drop source database if requested
        if drop_source:
            client.drop_database(source_db_name)
            print(f"✓ Dropped source database '{source_db_name}'")
        else:
            print(f"Source database '{source_db_name}' kept intact")
    
        return True
        
    except ConnectionFailure:
        print(f"✗ Failed to connect to MongoDB at {MONGO_HOST}:{MONGO_PORT}")
        return False
    except OperationFailure as e:
        print(f"✗ Operation failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    print("=" * 60)
    print("MongoDB Database Rename Utility")
    print("=" * 60)
    
    # You can either modify SOURCE_DB and TARGET_DB at the top,
    # or pass them as command line arguments
    if len(sys.argv) >= 3:
        source = sys.argv[1]
        target = sys.argv[2]
        drop = len(sys.argv) > 3 and sys.argv[3].lower() == '--drop-source'
    else:
        source = SOURCE_DB
        target = TARGET_DB
        drop = True
    
    print(f"\nSource Database: {source}")
    print(f"Target Database: {target}")
    print(f"MongoDB Host: {MONGO_HOST}:{MONGO_PORT}")
    print()
    
    success = rename_database(source, target, drop_source=drop)
    
    if success:
        print("\n✓ Database rename completed successfully!")
    else:
        print("\n✗ Database rename failed!")
        sys.exit(1) 
