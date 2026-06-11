from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from project import login_manager, mysql


class User(UserMixin):
    def __init__(self, userID, name, email):
        self.id = str(userID)
        self.userID = userID
        self.name = name
        self.email = email

    # def get_id(self):
    #     return str(self.id)

def rows(sql, params=None):
    cur = mysql.connection.cursor()
    try:
        cur.execute(sql, params or ())
        return cur.fetchall()
    finally:
        cur.close()


def row(sql, params=None):
    cur = mysql.connection.cursor()
    try:
        cur.execute(sql, params or ())
        return cur.fetchone()
    finally:
        cur.close()


def execute(sql, params=None):
    cur = mysql.connection.cursor()
    try:
        cur.execute(sql, params or ())
        mysql.connection.commit()
    finally:
        cur.close()


def next_id(table_name: str, id_column: str, prefix: str, width: int = 3) -> str:
    current = row(
        f"SELECT MAX(CAST(SUBSTRING({id_column}, %s) AS UNSIGNED)) AS max_num FROM {table_name}",
        (len(prefix) + 1,),
    )
    max_num = current["max_num"] or 0
    return f"{prefix}{max_num + 1:0{width}d}"


def fetch_collections():
    return rows(
        """
        SELECT collectionID AS collection_id,
               collectionName AS name,
               description
        FROM Collection
        ORDER BY collectionName
        """
    )


def fetch_item(item_id: str):
    return row(
        """
        SELECT ci.itemID AS item_id,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               ci.place,
               ci.languageGroup AS language_group,
               ci.status,
               ci.format,
               DATE_FORMAT(ci.dateAdded, '%%d %%M %%Y') AS date_added,
               ci.dateRecorded AS date_recorded,
               REPLACE(ci.imagePath, 'img/', '') AS image_filename,
               c.collectionName AS collection_name,
               c.description AS collection_description,
               cm.ownership,
               cm.accessLevel AS access_level,
               cm.culturalSensitivity AS cultural_sensitivity,
               cm.culturalNotes AS cultural_notes,
               cm.accessConditions AS access_conditions,
               cm.communityApprovalStatus AS community_approval
        FROM CollectionItem ci
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        WHERE ci.itemID = %s
        """,
        (item_id,),
    )

def fetch_user_requests(user_id):
    return rows(
        """
        SELECT 
            ar.requestID,
            ar.itemID,
            ar.requestDate,
            ar.requestStatus,
            ar.purpose,
            ci.title,
            ci.format,
            ci.status

        FROM accessrequest ar
        JOIN collectionitem ci ON ar.itemID = ci.itemID
        WHERE
            userID = %s
        ORDER BY requestDate
        """,
        (user_id,),
    )
def fetch_user_request(user_id, item_id):
    return row(
        """
        SELECT 
            ar.requestID,
            ar.itemID,
            ar.requestDate,
            ar.requestStatus,
            ar.purpose,
            ci.title,
            ci.format,
            ci.status

        FROM accessrequest ar
        JOIN collectionitem ci ON ar.itemID = ci.itemID
        WHERE
            ar.userID = %s
            AND ar.itemID = %s
        ORDER BY requestDate
        """,
        (user_id,item_id,),
    )

def create_user(name, email, password):
    password_hash = generate_password_hash(password)
    user_id = next_id("Users", "userID", "U")
    execute(
        """
        INSERT INTO Users
        (userID, name, email, passwordHash)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, name, email, password_hash),
    )
    return user_id


def get_user_by_email(email):
    return row(
        """
        SELECT userID, name, email, passwordHash
        FROM Users
        WHERE email = %s
        """,
        (email,),
    )


def get_user_by_id(userID):
    return row(
        """
        SELECT userID, name, email
        FROM Users
        WHERE userID = %s
        """,
        (userID,),
    )


def get_user_reviewer(userID):
    return row(
        """
        SELECT reviewerID,
               authorisationStatus,
               role
        FROM Reviewer
        WHERE userID = %s
        """,
        (userID,),
    )


def verify_user_password(email, password):
    user = get_user_by_email(email)

    if user is None:
        return None

    if check_password_hash(user["passwordHash"], password):
        return user

    return None


@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        return None

    return User(user["userID"], user["name"], user["email"])
