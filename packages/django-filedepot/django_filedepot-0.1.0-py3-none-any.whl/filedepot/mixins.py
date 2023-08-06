import hashlib

from .models import File

class FlowFileUploadMixin(object):
    def get_request_params(self, request):
        if request.method == 'GET':
            return request.query_params

        return request.data

    def handle_flow_request(self, request):
        request_params = self.get_request_params(request)

        # get flow variables
        flow_identifier = request_params.get('flowIdentifier')
        if not flow_identifier:
            raise IOError('A "flow_identifier" parameter must be supplied.')

        uuid = hashlib.sha1(flow_identifier.encode()).hexdigest()
        flow_chunk_number = int(request_params.get('flowChunkNumber'))
        flow_chunk_size = int(request_params.get('flowChunkSize'))
        flow_total_size = int(request_params.get('flowTotalSize'))
        flow_filename = request_params.get('flowFilename')
        flow_total_chunks = int(request_params.get('flowTotalChunks'))

        # TODO: This needs to be reviewed carefully. It has all sorts of implications
        # like, what happens if the user cancels one upload in a particular
        # field and then uploads a new file, what should we do?
        file, _ = File.objects.get_or_create(
            uuid=uuid,
            defaults={
                "user": request.user,
                "flow_filename": flow_filename,
                "flow_total_chunks": flow_total_chunks,
                "flow_chunk_size": flow_chunk_size,
                "flow_total_size": flow_total_size,
            }
        )
        if file.user.id != request.user.id:
            raise IOError('INTRUDER ALERT!')

        if (
            uuid != file.uuid
            or flow_filename != file.flow_filename
            or flow_total_chunks != file.flow_total_chunks
            or flow_chunk_size != file.flow_chunk_size
            or flow_total_size != file.flow_total_size
        ):
            file.delete_chunks()
            file.uuid = uuid
            file.flow_total_chunks = flow_total_chunks
            file.flow_chunk_size = flow_chunk_size
            file.flow_total_size = flow_total_size
            file.flow_filename = flow_filename
            file.save()

        # Sanity check to ensure the chunk directory exists and can be written to
        file.ensure_directory()

        result = {
            'file': file,
            'finished': False,
        }

        if request.method == 'GET':
            # TODO: eventually we can support resume, but for now let's skip
            if file.verify_chunk(flow_chunk_number):
                # Chunk is fine.
                result['status'] = 200
            else:
                # Chunk is not fine
                result['status'] = 204
        else:
            result['status'] = 200

            if not file.verify_chunk(flow_chunk_number):
                # Chunk does not yet exist
                chunk_filename = file.chunk_filename(flow_chunk_number)
                with open(chunk_filename, 'wb') as chunk_fd:
                    uploaded_chunk = request.FILES['file']
                    for chunk_chunk in uploaded_chunk.chunks():
                        chunk_fd.write(chunk_chunk)
                chunk_finished_filename = file.chunk_finished_filename(flow_chunk_number)
                with open(chunk_finished_filename, 'wb') as chunk_fd:
                    chunk_fd.write(b'1')

            if file.check_if_finished():
                file.join_chunks()
                result['finished'] = True
            else:
                result['finished'] = False

        return result
