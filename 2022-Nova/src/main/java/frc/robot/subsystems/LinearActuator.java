// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems;

import edu.wpi.first.wpilibj.Servo;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.commands.defaults.LinearActuatorDefault;

public class LinearActuator extends SubsystemBase {

  private Servo rightLinearActuator = new Servo(1);
  private Servo leftLinearActuator = new Servo(0);
  /** Creates a new LinearActuator. */
  public LinearActuator() {
    rightLinearActuator.setBounds(2, 1.5, 1.5, 1.5, 1);
  }

  public void init(){
    setDefaultCommand(new LinearActuatorDefault(this));
  }

  public double getActuatorPosition() {
    return rightLinearActuator.getPosition();
  }

  public void setActuator(double target){
    rightLinearActuator.setPosition(target);
    leftLinearActuator.setPosition(target);
  }

  @Override
  public void periodic() {
    // This method will be called once per scheduler run
  }
}