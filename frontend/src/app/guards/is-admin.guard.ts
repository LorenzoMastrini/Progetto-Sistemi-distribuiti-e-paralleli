import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { UserService } from '../services/user.service';

export const isAdminGuard: CanActivateFn = (route, state) => {
  if(inject(UserService).currentUser.isAdmin === 1) {
    return true;
  } else {
    return false;
  }
};