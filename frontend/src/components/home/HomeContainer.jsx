import {StyledHomeContainer} from "./styledHome";

const HomeContainer = () => {
    const [test, setTest] = useState("")

    const checkCon = () => {
        axios.post('./api/Utils/test.py').then(function () {
            setTest("it works")
        }).catch(function() {
            setTest("error")
        })
    }

    return (
        <StyledHomeContainer>
            <p>{test}</p>
            <button
                onClick={checkCon}
            >
                Home
            </button>
        </StyledHomeContainer>
    )
}

export default HomeContainer;