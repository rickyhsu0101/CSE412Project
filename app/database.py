import psycopg2
from passlib.hash import sha256_crypt
from datetime import datetime

class db():
    def __init__(self):
        this.connection = None
        try:
            this.connection = psycopg2.connect(host = "localhost", port = "8088", database = "GameDB")

        except _:
            print("Error connection with database")
            exit(0)

    #find if user exists
    def find_user(self, username):
        cursor = this.connection.cursor()

        sql = 'SELECT COUNT(*) FROM Client WHERE username = %s;'
        data = [username]
        cursor.execute(sql, data)

        result = cursor.fetchone()

        count = result[0]

        cursor.close()
        if count != 0:
            return True
        return False

    def create_user(self, username, password):
        cursor = this.connection.cursor()

        hashedpass = sha256_crypt.hash(password)
        timestamp = datetime.now()

        sql = 'INSERT INTO Client(username, hashedPass, lastUpdate) VALUES(%s, %s, %s) RETURNING userId;'
        data = [username, hashedpass, timestamp]

        cursor.execute(sql, data)

        result = cursor.fetchone()

        user_id = result[0]

        connection.commit()
        cursor.close()

        return user_id

    def user_authenticate(self, username, password):
        cursor = this.connection.cursor()

        sql = 'SELECT * FROM Client WHERE username = %s'
        data = [username]

        cursor.execute(sql, data)

        result = cursor.fetchone()
        cursor.close()
        if result == None:
            return (None, "Username not found")
        elif not sha256_crypt.verify(password, result[2]):
            return (None, "Wrong Password")
        else:
            return (result[0], "Success")


    def update_game_rating(self, game_name, rating):
        cursor = this.connection.cursor()

        sql = "UPDATE Game SET userRating = %s WHERE name = %s;";
        data = [rating, game_name]

        cursor.execute(sql, data)

        connection.commit()

        cursor.close()

        return

    def remove_user_like(self, game_name, user_id):
        cursor = this.connection.cursor()

        sql = "DELETE FROM Likes WHERE userId = %s AND gameId = (SELECT gameId FROM Game WHERE name = %s)";
        data = [user_id, game_name]

        cursor.execute(sql, data)

        connection.commit()

        cursor.close()

        return

    def select_games_liked_by_user(self, user_id):
        cursor = this.connection.cursor()

        sql = """SELECT Game.* 
                FROM Client, Likes, Game 
                WHERE Client.userId = Likes.userId 
                    AND Likes.gameId = Game.gameId
                    AND Client.userId = %s"""
        data = [user_id]

        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_published_by_publisher(self, publisher_name):
        cursor = this.connection.cursor()

        sql = """SELECT Game.*
                 FROM Game, HasPublisher, Publisher
                 WHERE Game.gameId = HasPublisher.gameId
                    AND HasPublisher.pubId = Publisher.pubId
                    AND Publisher.name = %s
                 ORDER BY releaseDate DESC;"""
        data = [user_id]

        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_release(self):
        cursor = this.connection.cursor()
        sql = 'SELECT * FROM Game ORDER BY releaseDate DESC;'

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_user_rating(self):
        cursor = this.connection.cursor()
        sql = 'SELECT * FROM Game ORDER BY userRating DESC;'

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_critic_rating(self):
        cursor = this.connection.cursor()
        sql = 'SELECT * FROM Game ORDER BY criticRating DESC;'

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_by_likes(self):
        cursor = this.connection.cursor()
        sql = """SELECT Game.*, T.likes_amount
                 FROM Game
                 LEFT JOIN (SELECT COUNT(userId) AS likes_amount, gameId
                            FROM Likes
                            GROUP BY gameId) AS T
                 ON Game.gameId = T.gameId
                 ORDER BY T.likes_amount DESC NULLS LAST;"""

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_sort_by_alph(self):
        cursor = this.connection.cursor()
        sql = 'SELECT * FROM Game ORDER BY name ASC;'

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def get_number_likes_for_game(self, game_id):
        cursor = this.connection.cursor()
        sql = """SELECT COUNT(userId)
                FROM (Likes
                    NATURAL JOIN Game)
                WHERE gameId = selectedGameId;"""

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_user_likes(self, username):
        cursor = this.connection.cursor()
        sql = """SELECT Game.*
                    FROM Client, Likes, Game
                    WHERE Client.userId = Likes.userId AND Likes.gameId = Game.gameId AND Client.username = %s;
                    """
        data = [username]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_by_platform(self, platform_id):
        cursor = this.connection.cursor()
        sql = """SELECT Game.*
                FROM Game, Platform, HasPlatform
                WHERE Game.gameId = HasPlatform.GameId 
                    AND Platform.platformId = HasPlatform.platformId 
                    AND Platform.platformId = %s;"""
        data = [platform_id]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results

    def select_games_by_developer(self, developer_id):
        cursor = this.connection.cursor()
        sql = """SELECT Game.*
                    FROM Game, Developer, HasDeveloper
                    WHERE Game.gameId = HasDeveloper.gameId 
                            AND Developer.devId = HasDeveloper.devId 
                            AND Developer.devId = %s;
                    """
        data = [developer_id]
        cursor.execute(sql,data)

        results = cursor.fetchall()

        cursor.close()

        return results

    
    def __del__(self):
        this.connection.close()




        