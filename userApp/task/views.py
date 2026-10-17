from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.


# Login page
def Login_page(request):
    return render(request, "Login_page.html")


@api_view(["POST"])
def login_user(request):
    role = request.data.get("role")
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"message": False, "error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    authenticated_user = authenticate(
        request, username=user.username, password=password
    )
    if authenticated_user is None:
        return Response(
            {"message" : False,"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED
        )

    if role == "user":

        if authenticated_user.is_staff:
            return Response(
                {"message": False, "error": "This is an Admin account. Select Admin."},
                status=status.HTTP_403_FORBIDDEN,
            )

    if role == "Admin":

        if not authenticated_user.is_staff:
            return Response(
                {"message": False, "error": "This is an user account. Select user."},
                status=status.HTTP_403_FORBIDDEN,
            )

    login(request, authenticated_user)

    return Response(
        {
            "message": True,
            "user_id": authenticated_user.id,
            "username": authenticated_user.username,
            "is_staff": authenticated_user.is_staff,
        }
    )


# sign up page
def Sign_up(request):
    return render(request, "Sign_up.html")


@api_view(["POST"])
def created_user(request):
    serial = CreateUserSerializer(data=request.data)

    if serial.is_valid():
        user = serial.save()
        login(request, user)
        return Response(
            {"message": True, "success": "User created successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(
        serial.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

def Home(request):
    return render(request, "home.html")


@api_view(["GET"])
def product_list(request):

    if not request.user.is_authenticated:
        return Response(
            {"error": "login required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if request.user.is_staff:
        products = product.objects.all()
    else:
        products = product.objects.filter(
            created_by=request.user
        )

    serial = getProductSerializers(products, many=True)

    return Response(serial.data)


def Addproduct(request):
    return render(request, "Addproduct.html")


@api_view(["POST"])
def create_product(request):

    if not request.user.is_authenticated:
        return Response(
            {"error": "Login required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    serial = getProductSerializers(data=request.data)

    if serial.is_valid():

        serial.save(created_by=request.user)

        return Response(
            serial.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serial.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["PATCH"])
def update_product(request, product_id):

    if not request.user.is_authenticated:
        return Response(
            {"message": False, "error": "Login required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        if request.user.is_staff:
            data = product.objects.get(id=product_id)
        else:
            data = product.objects.get(
                id=product_id,
                created_by=request.user
            )

    except product.DoesNotExist:
        return Response(
            {"message": False, "error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serial = CreateProductSerializers(
        data,
        data=request.data,
        partial=True
    )

    if serial.is_valid():
        serial.save()

        return Response(
            {"message": True, "data": serial.data},
            status=status.HTTP_200_OK
        )

    return Response(
        {"message": False, "error": serial.errors},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["DELETE"])
def delete_product(request, product_id):

    if not request.user.is_authenticated:
        return Response(
            {"error": "Login required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        if request.user.is_staff:
            item = product.objects.get(id=product_id)
        else:
            item = product.objects.get(
                id=product_id,
                created_by=request.user
            )

    except product.DoesNotExist:
        return Response(
            {"error": "Product not found or permission denied"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        return Response({"error" : e  })
    
    item.delete()

    return Response(
        {"message": True},
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_product(request, product_id):
    data = product.objects.get(id=product_id)
    seial = getProductSerializers(data)
    return Response(seial.data)