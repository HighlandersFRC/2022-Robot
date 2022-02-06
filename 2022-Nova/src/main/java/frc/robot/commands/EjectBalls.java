// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.subsystems.MagIntake;

public class EjectBalls extends CommandBase {
  /** Creates a new EjectBalls. */

  private MagIntake magIntake;
  private double upperPercent;
  private double lowerPercent;
  private double beltPercent;
  private double time = 0;
  private double initTime;

  public EjectBalls(MagIntake magIntake, double upperPercent, double lowerPercent, double beltPercent, double time) {
    this.magIntake = magIntake;
    this.upperPercent = upperPercent;
    this.lowerPercent = lowerPercent;
    this.beltPercent = beltPercent;
    this.time = time;
    addRequirements(magIntake);
    // Use addRequirements() here to declare subsystem dependencies.
  }

  // Called when the command is initially scheduled.
  @Override
  public void initialize() {
    initTime = Timer.getFPGATimestamp();
  }

  // Called every time the scheduler runs while the command is scheduled.
  @Override
  public void execute() {
    magIntake.setUpperFalcon(upperPercent);
    magIntake.setLowerFalcon(lowerPercent);
    magIntake.setBeltFalcon(beltPercent);
  }

  // Called once the command ends or is interrupted.
  @Override
  public void end(boolean interrupted) {}

  // Returns true when the command should end.
  @Override
  public boolean isFinished() {
    if(time != -1) {
      if(Timer.getFPGATimestamp() - initTime > time) {
        return true;
      }
    }
    return false;
  }
}
