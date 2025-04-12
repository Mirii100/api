from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Category, Item, Review, Order, OrderItem, Notification

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Profile
        fields = ('id', 'user', 'username', 'email', 'profile_picture', 'bio', 'location', 'date_joined')
        read_only_fields = ('user', 'date_joined')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'icon')

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ('id', 'item', 'user', 'username', 'rating', 'comment', 'created_at')
        read_only_fields = ('user', 'created_at')

class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = ('id', 'title', 'description', 'category', 'category_name', 
                  'created_by', 'created_by_username', 'price', 'image', 
                  'created_at', 'updated_at', 'is_available', 'reviews', 
                  'average_rating')
        read_only_fields = ('created_by', 'created_at', 'updated_at')
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

class OrderItemSerializer(serializers.ModelSerializer):
    item_title = serializers.CharField(source='item.title', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'item', 'item_title', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'user', 'username', 'status', 'created_at', 'updated_at', 
                  'shipping_address', 'total_amount', 'items')
        read_only_fields = ('user', 'created_at', 'updated_at')

class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.DictField(), write_only=True)
    
    class Meta:
        model = Order
        fields = ('shipping_address', 'items')
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Calculate total amount
        total_amount = 0
        for item_data in items_data:
            item_id = item_data.get('item_id')
            quantity = item_data.get('quantity', 1)
            
            try:
                item = Item.objects.get(id=item_id)
                total_amount += item.price * quantity
            except Item.DoesNotExist:
                raise serializers.ValidationError(f"Item with id {item_id} does not exist")
        
        # Create order
        order = Order.objects.create(
            user=user,
            shipping_address=validated_data['shipping_address'],
            total_amount=total_amount
        )
        
        # Create order items
        for item_data in items_data:
            item_id = item_data.get('item_id')
            quantity = item_data.get('quantity', 1)
            
            item = Item.objects.get(id=item_id)
            OrderItem.objects.create(
                order=order,
                item=item,
                quantity=quantity,
                price=item.price
            )
        
        return order

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user', 'title', 'message', 'is_read', 'created_at')
        read_only_fields = ('user', 'created_at')
