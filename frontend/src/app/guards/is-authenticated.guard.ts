import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { UserService } from '../services/user.service';

export const isAuthenticatedGuard: CanActivateFn = (route, state) => {
  if(inject(UserService).currentUser.token != undefined) {
    return true;
  } else {
    return false;
  }
};
