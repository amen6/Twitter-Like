function like(id) {
  addEventListener('click', () => {
    form = new FormData();
    form.append("id", id);
     fetch("/like/", {
       method: "POST",
       body: form,
     })
     .then((res) => res.json())
      .then((res) => {
        console.log(res);
      })
  })
}
