// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems;

import com.ctre.phoenix.motorcontrol.ControlMode;
import com.ctre.phoenix.motorcontrol.InvertType;
import com.ctre.phoenix.motorcontrol.can.TalonFX;

import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.commands.defaults.MagazineDefault;
import frc.robot.tools.PneumaticsControl;

public class MagIntake extends SubsystemBase {

  private PneumaticsControl pneumatics;
  private final TalonFX intakeMotor = new TalonFX(12);

  /** Creates a new MagIntake. */
  public MagIntake(PneumaticsControl pneumatics) {
    this.pneumatics = pneumatics;
  }

  private final TalonFX beltFalcon = new TalonFX(13);
    private final TalonFX lowerFalcon = new TalonFX(14);
    private final TalonFX upperFalcon = new TalonFX(15);

    private final DigitalInput lowerBeamBreak = new DigitalInput(0);
    private final DigitalInput upperBeamBreak = new DigitalInput(1);

    public Boolean getLowerBeamBreak() {
        return lowerBeamBreak.get();
    }

    public Boolean getUpperBeamBreak() {
        return upperBeamBreak.get();
    }

    public void moveMagazine() {  
        if(!getUpperBeamBreak()){
          lowerFalcon.set(ControlMode.PercentOutput, 0.0);
        } else {
          if(!getLowerBeamBreak()){
            lowerFalcon.set(ControlMode.PercentOutput, -0.3);
          } else{
            lowerFalcon.set(ControlMode.PercentOutput, 0.0);
          }
        }
           
    }

    public void init() {
        upperFalcon.setInverted(InvertType.InvertMotorOutput);
        setDefaultCommand(new MagazineDefault(this));
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

    public void setIntakeUp() {
      pneumatics.setIntakeUp();
    }
  
    public void setIntakeDown() {
      pneumatics.setIntakeDown();
    }
  
    public void setIntakePercent(double percent) {
      intakeMotor.set(ControlMode.PercentOutput, percent);
    }
}
