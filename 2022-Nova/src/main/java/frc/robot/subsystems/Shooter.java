// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems;

import com.ctre.phoenix.motorcontrol.ControlMode;
import com.ctre.phoenix.motorcontrol.FeedbackDevice;
import com.ctre.phoenix.motorcontrol.InvertType;
import com.ctre.phoenix.motorcontrol.NeutralMode;
import com.ctre.phoenix.motorcontrol.SupplyCurrentLimitConfiguration;
import com.ctre.phoenix.motorcontrol.can.TalonFX;
import com.revrobotics.CANSparkMax.IdleMode;

import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.Constants;
import frc.robot.commands.defaults.IntakeDefault;
import frc.robot.commands.defaults.ShooterDefault;
import frc.robot.tools.PneumaticsControl;

public class Shooter extends SubsystemBase {

 private final TalonFX leftShooter = new TalonFX(10);
 private final TalonFX rightShooter = new TalonFX(9);

  /** Creates a new Intake. */
  public Shooter() {
    
  }

  public void init() {
     leftShooter.setNeutralMode(NeutralMode.Coast);
     rightShooter.setNeutralMode(NeutralMode.Coast);
     rightShooter.setInverted(InvertType.InvertMotorOutput);
    // rightShooter.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor, 0, 0);
    // // rightShooter.configPeakOutputForward(0.7);
    // rightShooter.configClosedLoopPeakOutput(0, 0.7);
    // // rightShooter.configPeakOutputReverse(-0.7);
    // rightShooter.configVoltageCompSaturation(11.7);
    // rightShooter.enableVoltageCompensation(true);
    // rightShooter.setSensorPhase(true);
    // rightShooter.selectProfileSlot(0, 0);
    rightShooter.config_kF(0, 0);
    rightShooter.config_kP(0, 0.17);
    rightShooter.config_kI(0, 0.001);
    rightShooter.config_kD(0, 0);
    leftShooter.set(ControlMode.Follower, 9);
    setDefaultCommand(new ShooterDefault(this));
    // rightShooter.configSupplyCurrentLimit(new SupplyCurrentLimitConfiguration(true, 80, 0, 0));
  }

  public void zeroShooterEncoder() {
    // rightShooter.setSelectedSensorPosition(0);
    leftShooter.setSelectedSensorPosition(0);
}


  public void setShooterPercent(double percent) {
    rightShooter.set(ControlMode.PercentOutput, percent);
  }

  public void setShooterRPM(double rpm) {
    System.out.println(Constants.shooterRPMToUnitsPer100MS(rpm));
    rightShooter.set(ControlMode.Velocity, Constants.shooterRPMToUnitsPer100MS(rpm));

    // rightShooter.set(ControlMode.PercentOutput, 0.5);
}

public double getShooterRPM(){
  return Constants.unitsPer100MsToRPM(rightShooter.getSelectedSensorVelocity());
}

  @Override
  public void periodic() {
    // This method will be called once per scheduler run
  }
}
