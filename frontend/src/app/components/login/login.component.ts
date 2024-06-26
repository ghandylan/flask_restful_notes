import {Component} from '@angular/core';
import {Router} from "@angular/router";
import {HttpClient} from "@angular/common/http";
import {UserService} from "../../../services/user.service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  private userService: UserService;

  constructor(private router: Router, private http: HttpClient, userService: UserService) {
    this.userService = userService;
  }

  navigateToRegister() {
    this.router.navigate(['/register']);
  }

  greetUser() {
    const token = localStorage.getItem('access_token');
    if (token) {
      const decodedToken = JSON.parse(atob(token.split('.')[1]));
      if ('sub' in decodedToken && 'username' in decodedToken.sub) {
        alert(`Hello, ${decodedToken.sub.username}!`);
        console.log(decodedToken.sub.username);
      } else {
        alert('Username claim is not present in the token.');
      }
    } else {
      alert('No user is currently logged in.');
    }
  }

  onSubmit(username: string, password: string) {
    this.userService.loginUser(username, password).subscribe(
      (response: any) => {
        localStorage.setItem('access_token', response.access_token);
        this.greetUser();
        this.router.navigate(['/notes']);
      },
      (error) => {
        if (error.status === 401) {
          // If the error status is 401 (Unauthorized), show an alert dialog
          alert('Invalid credentials. Please try again.');
        } else {
          // For any other error, log it to the console
          console.error(error);
        }
      }
    );
  }
}
