using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public GameObject Player;
    public GameObject EnemyPrefab;

    public int SpawnTime = 30;
    private int counter;

    // Start is called before the first frame update
    void Start()
    {
        counter = 0;   
    }

    void FixedUpdate() {
        // If we can spawn the Ball
        if (counter > SpawnTime) {
            // We generate a random x coordinate for the Ball
            float xPosition = Random.Range(-10, 10);
            float zPosition = Random.Range(-10, 10);

            var position = Player.transform.position + new Vector3(xPosition, 0, zPosition);
            position.x = Mathf.Clamp(position.x, -20, +20);
            position.z = Mathf.Clamp(position.z, -20, +20);


            // We instantiate a new Ball at the generated axis while keeping the Y and Z axes constant
            var enemy = Instantiate(EnemyPrefab, transform.position + new Vector3(xPosition, 3, zPosition), Quaternion.identity, gameObject.transform);
            var enemyScript = enemy.GetComponent<FollowPlayer>();
            enemyScript.Player = Player;
            // We make sure that the Ball is properly scaled
           // ball.transform.localScale = new Vector3(1, 1, 1);

            // We tell the program to destroy the Ball after 10 seconds have passed and reset the counter
            //Destroy(ball, 10);
            counter = 0;
        }
        else {
            counter++;
        }

    }

    public void Despawn() {
        int numberOfChildren = transform.childCount;

        for (int i = 0; i < numberOfChildren; i++) {
            if (transform.GetChild(i).tag == "Enemy") {
                Destroy(transform.GetChild(i).gameObject);
            }
        }
    }
}
