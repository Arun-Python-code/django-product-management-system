from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def Login_page(request):
    """Render the page containing the login form."""
    return render(request, "Login_page.html")


@api_view(["POST"])
def login_user(request):
    """Authenticate submitted credentials and create a login session."""
    # Read the role and credentials submitted in the JSON request body.
    role = request.data.get("role")
    email = request.data.get("email")
    password = request.data.get("password")

    # Find the account by email before asking Django to validate its password.
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Use the same response for unknown emails and invalid passwords.
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

    # Ensure the selected login role matches the account's staff status.
    if role == "user":

        if authenticated_user.is_staff:
            return Response(
                {"message": False, "error": "This is an Admin account. Select Admin."},
                status=status.HTTP_403_FORBIDDEN,
            )

    # Only staff accounts may continue when the Admin role was selected.
    if role == "Admin":

        if not authenticated_user.is_staff:
            return Response(
                {"message": False, "error": "This is an user account. Select user."},
                status=status.HTTP_403_FORBIDDEN,
            )

    # Store the authenticated account in Django's session.
    login(request, authenticated_user)

    # Return account details used by the client after a successful login.
    return Response(
        {
            "message": True,
            "user_id": authenticated_user.id,
            "username": authenticated_user.username,
            "is_staff": authenticated_user.is_staff,
        }
    )


def Sign_up(request):
    """Render the page containing the account registration form."""
    return render(request, "Sign_up.html")


@api_view(["POST"])
def created_user(request):
    """Validate registration data, create an account, and start its session."""
    # The serializer validates submitted fields and hashes the password on save.
    serial = CreateUserSerializer(data=request.data)

    if serial.is_valid():
        user = serial.save()
        # Sign in the newly registered account immediately.
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
    """Render the page where the product list is loaded by JavaScript."""
    return render(request, "home.html")


@api_view(["GET"])
def product_list(request):
    """Return products visible to the signed-in user as serialized JSON."""
    # Require a session before exposing product data.
    if not request.user.is_authenticated:
        return Response(
            {"error": "login required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Staff can list every product; other users only see their own rows.
    if request.user.is_staff:
        products = product.objects.all()
    else:
        products = product.objects.filter(
            created_by=request.user
        )

    # Serialize the queryset into the JSON response shape expected by the client.
    serial = getProductSerializers(products, many=True)

    return Response(serial.data)


def Addproduct(request):
    """Render the form used to create or edit a product."""
    return render(request, "Addproduct.html")


@api_view(["POST"])
def create_product(request):
    """Validate and create a product owned by the current user."""
    # Do not accept product-creation requests without an authenticated session.
    if not request.user.is_authenticated:
        return Response(
            {"error": "Login required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Validate the submitted product fields before inserting a database row.
    serial = getProductSerializers(data=request.data)

    if serial.is_valid():
        # Set the owner from the session rather than trusting client-supplied data.
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
    """Partially update a product the current user is allowed to manage."""
    # Require a signed-in user before accessing product records.
    if not request.user.is_authenticated:
        return Response(
            {"message": False, "error": "Login required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        # Staff may update any product; regular users may update only their own.
        if request.user.is_staff:
            data = product.objects.get(id=product_id)
        else:
            data = product.objects.get(
                id=product_id,
                created_by=request.user
            )

    except product.DoesNotExist:
        # Return 404 when the product is missing or outside the user's queryset.
        return Response(
            {"message": False, "error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # partial=True allows PATCH requests to omit fields that are not being changed.
    serial = CreateProductSerializers(
        data,
        data=request.data,
        partial=True
    )

    if serial.is_valid():
        # Save only fields accepted by the serializer and return the updated values.
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
    """Delete a product when the requester is its owner or a staff user."""
    # Require an authenticated session before looking up the product.
    if not request.user.is_authenticated:
        return Response(
            {"error": "Login required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        # Staff may delete any product; regular users may delete only their own.
        if request.user.is_staff:
            item = product.objects.get(id=product_id)
        else:
            item = product.objects.get(
                id=product_id,
                created_by=request.user
            )

    except product.DoesNotExist:
        # Avoid revealing whether a product exists outside this user's access.
        return Response(
            {"error": "Product not found or permission denied"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        # Return other lookup errors using the existing response behavior.
        return Response({"error" : e  })
    
    # Remove the authorized row and confirm completion to the client.
    item.delete()

    return Response(
        {"message": True},
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_product(request, product_id):
    """Return serialized details for the product identified by its database ID."""
    # Fetch the requested row and serialize the fields used to fill the edit form.
    data = product.objects.get(id=product_id)
    seial = getProductSerializers(data)
    return Response(seial.data)