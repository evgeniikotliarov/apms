class NavBar extends Component {
  state = {
    login: ''
  };

  componentWillMount = () => {
    Application.userUseCase.getProfile()
      .subscribe(profile => {
        this.setState({login: profile.email});
      });
  };
  render = () => {
    return (
      <div className="Navbar">
        <ul className="navigation-bar">
          <li className="tab active-tab"><a href="#">Time sheet</a></li>
          <li className="tab"><a href="#">Users</a></li>
          <li className="tab"><a href="#">Statistic</a></li>
          <li className="log-box">
            <a className="login" href="#">{this.state.login}</a>
            <span/>
            <a className="log-out" href="#">Log out</a>
          </li>
        </ul>
      </div>
    )
  }
}

export default NavBar;