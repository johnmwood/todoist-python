# -*- coding: utf-8 -*-
from .. import models
from .generic import Manager, AllMixin, GetByIdMixin, SyncMixin


class ProjectsManager(Manager, AllMixin, GetByIdMixin, SyncMixin):

    state_name = 'projects'
    object_type = 'project'

    def add(self, name, **kwargs):
        """
        Creates a local project object.
        """
        obj = models.Project({'name': name}, self.api)
        obj.temp_id = obj['id'] = '$' + self.api.generate_uuid()
        obj.data.update(kwargs)
        self.state[self.state_name].append(obj)
        cmd = {
            'type': 'project_add',
            'temp_id': obj.temp_id,
            'uuid': self.api.generate_uuid(),
            'args': obj.data,
        }
        self.queue.append(cmd)
        return obj

    def update(self, project_id, **kwargs):
        """
        Updates a project remotely.
        """
        obj = self.get_by_id(project_id)
        if obj:
            obj.data.update(kwargs)

        args = {'id': project_id}
        args.update(kwargs)
        cmd = {
            'type': 'project_update',
            'uuid': self.api.generate_uuid(),
            'args': args,
        }
        self.queue.append(cmd)

    def delete(self, project_ids):
        """
        Deletes a project remotely.
        """
        cmd = {
            'type': 'project_delete',
            'uuid': self.api.generate_uuid(),
            'args': {
                'ids': project_ids,
            },
        }
        self.queue.append(cmd)

    def archive(self, project_id):
        """
        Marks project as archived remotely.
        """
        cmd = {
            'type': 'project_archive',
            'uuid': self.api.generate_uuid(),
            'args': {
                'id': project_id,
            },
        }
        self.queue.append(cmd)

    def unarchive(self, project_id):
        """
        Marks project as not archived remotely.
        """
        cmd = {
            'type': 'project_unarchive',
            'uuid': self.api.generate_uuid(),
            'args': {
                'id': project_id,
            },
        }
        self.queue.append(cmd)

    def update_orders_indents(self, ids_to_orders_indents):
        """
        Updates the orders and indents of multiple projects remotely.
        """
        cmd = {
            'type': 'project_update_orders_indents',
            'uuid': self.api.generate_uuid(),
            'args': {
                'ids_to_orders_indents': ids_to_orders_indents,
            },
        }
        self.queue.append(cmd)

    def share(self, project_id, email, message=''):
        """
        Shares a project with a user.
        """
        cmd = {
            'type': 'share_project',
            'temp_id': self.api.generate_uuid(),
            'uuid': self.api.generate_uuid(),
            'args': {
                'project_id': project_id,
                'email': email,
            },
        }
        self.queue.append(cmd)

    def take_ownership(self, project_id):
        """
        Takes ownership of a shared project.
        """
        cmd = {
            'type': 'take_ownership',
            'uuid': self.api.generate_uuid(),
            'args': {
                'project_id': project_id,
            },
        }
        self.queue.append(cmd)
