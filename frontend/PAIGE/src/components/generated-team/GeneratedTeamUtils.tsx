export function capitalizeFirstLetter(givenString: string) {
  return (
    String(givenString).charAt(0).toUpperCase() + String(givenString).slice(1)
  );
}
