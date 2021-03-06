"""
Señales eventos base de datos
"""

from asgiref.sync import async_to_sync
# third-party
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
# Django
from django.dispatch import receiver

# local Django
from chat.models import Room
from chat.serializers import RoomHeavySerializer


@receiver(post_save, sender=Room)
def room_upsert(sender, instance, **kwargs):
    """
    ...
    """
    group_name: str = 'rooms'
    channel_layer = get_channel_layer()
    serializer = RoomHeavySerializer(instance)
    # print(serializer.data)

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'room_event',
            'method': 'U',
            'data': serializer.data,
        }
    )


@receiver(post_delete, sender=Room)
def room_deleted(sender, instance, **kwargs):
    """
    ...
    """
    group_name: str = 'rooms'
    channel_layer = get_channel_layer()
    serializer = RoomHeavySerializer(instance)

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'room_event',
            'method': 'D',
            'data': serializer.data,
        }
    )
