using System.Collections;
using System.Collections.Generic;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using UnityEngine;

public class MyAgent : Agent
{
    //Rigidbody rigidBody;
    public float speed = 1;
    public GameObject Laser;
    public Spawner Spawner;
    private float fireRate = 0.5f;
    private float lastShot = 0;


    // Start is called before the first frame update
    void Start() {
    }

    public override void OnEpisodeBegin() {
        transform.localPosition = new Vector3(0, 3, 0);
    }

    public override void CollectObservations(VectorSensor sensor) {      
       
    }

    private void Shoot() {
        var laserObj = Instantiate(Laser, new Vector3(transform.position.x, transform.position.y, transform.position.z), transform.rotation);
        laserObj.transform.Translate(Vector3.forward * 1.5f);        
    }

    public override void OnActionReceived(ActionBuffers actions) {
        var actionContinuous = actions.ContinuousActions;
        var actionShoot = actions.DiscreteActions[0];

        float actionSpeed = (actionContinuous[0] + 1) / 2; // [0, +1]
        float actionSteering = actionContinuous[1]; // [-1, +1]

        transform.Translate(actionSpeed * Vector3.forward * speed * Time.fixedDeltaTime);
        transform.rotation = Quaternion.Euler(new Vector3(0, actionSteering * 180, 0));

        if (actionShoot == 1) {
            if(Time.time > fireRate + lastShot) {
                Shoot();
                lastShot = Time.time;
            }
        }

        AddReward(0.01f);
    }

    public override void Heuristic(in ActionBuffers actionsOut) {
        ActionSegment<float> actionsContinuous = actionsOut.ContinuousActions;
        ActionSegment<int> actionsDiscrete = actionsOut.DiscreteActions;

        actionsDiscrete[0] = 0;

        actionsContinuous[0] = -1;
        actionsContinuous[1] = 0;

        if (Input.GetKey("w"))
            actionsContinuous[0] = 1;

        if (Input.GetKey("s"))
            actionsContinuous[0] = -1;

        if (Input.GetKey("d"))
            actionsContinuous[1] = +0.5f;

        if (Input.GetKey("a"))
            actionsContinuous[1] = -0.5f;

        if (Input.GetKey("space"))
            actionsDiscrete[0] = 1;
    }

    private void OnTriggerEnter(Collider other) {
        if (other.tag == "Wall") {
            AddReward(-1);
            Spawner.Despawn();
            EndEpisode();
        }
        else if (other.tag == "Enemy") {
            AddReward(-1);
            Spawner.Despawn();
            EndEpisode();
        }
    }

}
