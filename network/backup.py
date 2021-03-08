if request.method == "POST":
    form = write(request.POST)
    if form.is_valid():
        text = form.cleaned_data['text']
        post.objects.create(user=request.user, text=text)
        added = "Post has been added, " + "<a href='/'>Home</a>"
        HttpResponse(added)
    error = "Error Occured, go back to " + f"<a href='/'>Home</a>"
    return HttpResponse(error)
else:
    context = {
        'write':write
    }
    return render(render, "network/create.html")
//////////////////////////////////////////////////////////////////////////////////////
    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)


    data = json.loads(request.body)
    # Get contents of email
    body = data.get("body", "")
    if body == [""]:
        return JsonResponse({
            "error": "Empty post."
        }, status=400)

    post = post(
        user=request.user,
        text=body
    )
    post.save()
    return JsonResponse({"message": "Email sent successfully."}, status=201)
