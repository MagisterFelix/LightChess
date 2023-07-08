const handleErrors = (validation, data, setFieldError, setNonFieldError) => {
  if (Array.isArray(data)) {
    Array.from(data).forEach(
      (obj) => Object.entries(obj).forEach(
        (entry) => {
          const [field, msg] = entry;
          if (field in validation) {
            setFieldError(field, { message: msg });
          } else {
            setNonFieldError({ type: 'error', message: msg });
          }
        },
      ),
    );
  } else {
    setNonFieldError({ type: 'error', message: data });
  }
};

export default handleErrors;
