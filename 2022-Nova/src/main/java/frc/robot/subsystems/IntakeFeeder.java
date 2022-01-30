// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems;

import com.ctre.phoenix.motorcontrol.ControlMode;
import com.ctre.phoenix.motorcontrol.InvertType;
import com.ctre.phoenix.motorcontrol.can.TalonFX;

import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.commands.defaults.IntakeFeederDefault;
import frc.robot.tools.PneumaticsControl;

public class IntakeFeeder extends SubsystemBase {

    private PneumaticsControl pneumatics;

    private final TalonFX intakeMotor = new TalonFX(12);

    private final TalonFX beltFalcon = new TalonFX(13);
    private final TalonFX lowerFalcon = new TalonFX(14);
    private final TalonFX upperFalcon = new TalonFX(15);
    private final DigitalInput bottomBeamBreak = new DigitalInput(0);
    private final DigitalInput topBeamBreak = new DigitalInput(1);

    private int ballCount;

    /** Creates a new Intake. */
    public IntakeFeeder(PneumaticsControl pneumatics) {
      this.pneumatics = pneumatics;
    }

    public void init() {
        upperFalcon.setInverted(InvertType.InvertMotorOutput);
        ballCount = 0;
        setDefaultCommand(new IntakeFeederDefault(this));
    }

    public void setBeltFalcon(double percent) {
        beltFalcon.set(ControlMode.PercentOutput, percent);
    }

    public void setLowerFalcon(double percent) {
        lowerFalcon.set(ControlMode.PercentOutput, -percent);
    }

    public void setUpperFalcon(double percent) {
        upperFalcon.set(ControlMode.PercentOutput, percent);
    }

    public int getBallCount() {
      return ballCount;
    }

    public void setBallCount(int num) {
      ballCount = num;
    }

    public void incrementBallCount() {
      ballCount ++;
    }

    public boolean getTopBeamBreak() {
        return topBeamBreak.get();
    }

    public boolean getBottomBeamBreak() {
        return bottomBeamBreak.get();
    }

    public void setIntakeUp() {
        pneumatics.setIntakeUp();
    }

    public void setIntakeDown() {
        pneumatics.setIntakeDown();
    }

  public void setIntakePercent(double percent) {
    intakeMotor.set(ControlMode.PercentOutput, percent);
  }

  @Override
  public void periodic() {
    SmartDashboard.putBoolean("Top BB", topBeamBreak.get());
    SmartDashboard.putBoolean("Bottom BB", bottomBeamBreak.get());
    SmartDashboard.putNumber("Ball Count", ballCount);
  }

  public void teleopInit() {
    ballCount = 0;
  }
}
