import api from './api';
import authApi from './auth';
import tasksApi from './tasks';

export {
  api,
  authApi,
  tasksApi
};

export default {
  api,
  auth: authApi,
  tasks: tasksApi
};
