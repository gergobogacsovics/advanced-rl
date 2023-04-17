using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Shoot : MonoBehaviour
{

    private float speed = 30;

    private void Start() {
        Destroy(gameObject, 3);    
    }

    private void FixedUpdate() {
        transform.Translate(Vector3.forward * speed * Time.fixedDeltaTime);
    }

    private void OnTriggerEnter(Collider other) {
        if (other.tag == "Enemy")
            Destroy(other.gameObject);
    }
}
