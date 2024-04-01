import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {User} from "../../../models/user";
import {UserService} from "../../../services/user.service";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup;
  userService: UserService;

  user: User = {
    id: 0,
    username: '',
    password: ''
  }

  constructor(private router: Router, private formBuilder: FormBuilder, userService: UserService) {
    this.userService = userService
  }

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(1)]],
      password_confirmation: ['', Validators.required]
    });
  }

  navigateToLogin() {
    this.router.navigate(['/login']);
  }

  onSubmit(user: User) {
    if (this.registerForm.valid) {
      const user = this.registerForm.value;
      this.userService.registerUser(user).subscribe(
        (response: any) => {
          this.router.navigate(['/login']);
          console.log(user);
        },
        (error) => {
          if (error.status === 409) {
            // If the error status is 409 (Unauthorized), show an alert dialog
            alert('user already exists');
          } else {
            // For any other error, log it to the console
            alert(error)
          }
        }
      );
    }
  }
}
