// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems;

import com.ctre.phoenix.motorcontrol.ControlMode;
import com.ctre.phoenix.motorcontrol.InvertType;
import com.ctre.phoenix.motorcontrol.NeutralMode;
import com.ctre.phoenix.motorcontrol.can.TalonFX;
import com.revrobotics.CANSparkMax.IdleMode;

import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.commands.defaults.IntakeFeederDefault;
import frc.robot.commands.defaults.ShooterDefault;
import frc.robot.tools.PneumaticsControl;

public class Shooter extends SubsystemBase {

  private final TalonFX leftShooter = new TalonFX(10);
  private final TalonFX rightShooter = new TalonFX(9);

  /** Creates a new Intake. */
  public Shooter() {
    
  }

  public void init() {
    // rightShooter.set(ControlMode.Follower, 10);
    leftShooter.setNeutralMode(NeutralMode.Coast);
    rightShooter.setNeutralMode(NeutralMode.Coast);
    rightShooter.setInverted(InvertType.InvertMotorOutput);
    setDefaultCommand(new ShooterDefault(this));
  }

  public void setShooterPercent(double percent) {
    leftShooter.set(ControlMode.PercentOutput, percent);
    rightShooter.set(ControlMode.PercentOutput, percent);
  }

  @Override
  public void periodic() {
    // This method will be called once per scheduler run
  }
}
