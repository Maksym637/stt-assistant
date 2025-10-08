export const fetchAccessToken = async (getAccessTokenSilently) => {
  try {
    const token = await getAccessTokenSilently();
    console.log(token);
  } catch (error) {
    console.log(`Error occured - ${error}`);
  }
};
