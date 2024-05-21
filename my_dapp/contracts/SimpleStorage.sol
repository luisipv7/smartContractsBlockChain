pragma solidity ^0.8.0;

contract BirthCertificate {
    struct Certificate {
        string name;
        string dateOfBirth;
        string placeOfBirth;
        string parents;
    }

    mapping(uint256 => Certificate) private certificates;
    uint256 private nextId = 1;
    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function createCertificate(
        string memory name,
        string memory dateOfBirth,
        string memory placeOfBirth,
        string memory parents
    ) public onlyOwner returns (uint256) {
        certificates[nextId] = Certificate(
            name,
            dateOfBirth,
            placeOfBirth,
            parents
        );
        nextId++;
        return nextId - 1;
    }

    function getCertificate(
        uint256 id
    )
        public
        view
        returns (string memory, string memory, string memory, string memory)
    {
        Certificate memory cert = certificates[id];
        return (cert.name, cert.dateOfBirth, cert.placeOfBirth, cert.parents);
    }
}
