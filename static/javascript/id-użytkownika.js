function setUserID(id) {
  localStorage.setItem('userId', id);
}

function getUserID() {
  return localStorage.getItem('userId');
}

if (!userId) {
  setUserID(1);
}
console.log("ID użytkownika:", getUserID());
