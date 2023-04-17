using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FollowPlayer : MonoBehaviour
{
    public GameObject Player;
    public float speed = 2;
    public float rotationSpeed = 2;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    // Source: https://answers.unity.com/questions/56251/make-object-move-tofollow-another-object-plus-turn.html
    private void FixedUpdate() {
        //rotate to look at the player
        transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(Player.transform.position - transform.position), Time.fixedDeltaTime * rotationSpeed);

        //move towards the player
        transform.localPosition += transform.forward * Time.fixedDeltaTime * speed;
    }

}
