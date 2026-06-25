function Sidebar() {
  return (
    <div className="sidebar">
      <div className="logo">
        <h2>Securetrace</h2>
      </div>

      <div className="menu">
        <div
          className="menu-item"
          onClick={() => {
            localStorage.setItem("page", "dashboard");
            window.location.reload();
          }}
        >
          Dashboard
        </div>

        <div
          className="menu-item"
          onClick={() => {
            localStorage.setItem("page", "threat");
            window.location.reload();
          }}
        >
          Threat Queue
        </div>
      </div>
    </div>
  );
}

export default Sidebar;