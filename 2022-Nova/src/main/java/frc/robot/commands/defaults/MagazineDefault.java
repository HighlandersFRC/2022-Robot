// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands.defaults;

import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.subsystems.MagIntake;

public class MagazineDefault extends CommandBase {
  /** Creates a new MagIntakeDefault. */
  private MagIntake magIntake;
  public MagazineDefault(MagIntake magIntake) {
    this.magIntake = magIntake;
    addRequirements(magIntake);
    // Use addRequirements() here to declare subsystem dependencies.
  }

  // Called when the command is initially scheduled.
  @Override
  public void initialize() {}

  // Called every time the scheduler runs while the command is scheduled.
  @Override
  public void execute() {
    magIntake.setUpperFalcon(0);
    magIntake.setLowerFalcon(0);
    magIntake.setBeltFalcon(0);
    magIntake.setIntakePercent(0);
    // magIntake.moveMagazine();
    magIntake.setIntakeUp();
  }

  // Called once the command ends or is interrupted.
  @Override
  public void end(boolean interrupted) {}

  // Returns true when the command should end.
  @Override
  public boolean isFinished() {
    return false;
  }
}
