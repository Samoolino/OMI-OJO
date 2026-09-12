// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title Blue-Ether DMRV Evidence Registry
/// @notice Anchors hashes and verification state for observed environmental evidence.
/// @dev Raw telemetry, laboratory reports and forecast payloads remain off-chain.
contract BlueEtherDMRVRegistry {
    bytes32 public constant SUBMITTER_ROLE = keccak256("SUBMITTER_ROLE");
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE");

    enum EvidenceState { NONE, SUBMITTED, VERIFIED, REJECTED }
    enum MeasurementClass { OBSERVED, FORECAST }

    struct Evidence {
        bytes32 evidenceId;
        bytes32 payloadHash;
        bytes32 sourceHash;
        bytes32 metadataHash;
        bytes32 lcdaId;
        uint64 observedAt;
        uint64 submittedAt;
        uint256 rainfallMmX100;
        uint256 yieldLitresX100;
        MeasurementClass measurementClass;
        EvidenceState state;
        address submitter;
        address verifier;
    }

    address public owner;
    bool public paused;
    mapping(bytes32 => mapping(address => bool)) private roles;
    mapping(bytes32 => Evidence) private evidence;
    mapping(bytes32 => bool) public evidenceExists;

    event EvidenceSubmitted(bytes32 indexed evidenceId, bytes32 indexed payloadHash, bytes32 indexed lcdaId, uint64 observedAt, address submitter);
    event EvidenceVerified(bytes32 indexed evidenceId, address indexed verifier, uint64 verifiedAt);
    event EvidenceRejected(bytes32 indexed evidenceId, address indexed verifier, uint64 rejectedAt);
    event RoleUpdated(bytes32 indexed role, address indexed account, bool enabled);
    event PauseUpdated(bool paused);

    modifier onlyOwner() {
        require(msg.sender == owner, "NOT_OWNER");
        _;
    }

    modifier onlyRole(bytes32 role) {
        require(roles[role][msg.sender], "NOT_AUTHORIZED");
        _;
    }

    modifier whenNotPaused() {
        require(!paused, "PAUSED");
        _;
    }

    constructor(address initialOwner) {
        require(initialOwner != address(0), "ZERO_OWNER");
        owner = initialOwner;
        roles[SUBMITTER_ROLE][initialOwner] = true;
        roles[VERIFIER_ROLE][initialOwner] = true;
    }

    function setRole(bytes32 role, address account, bool enabled) external onlyOwner {
        require(account != address(0), "ZERO_ACCOUNT");
        roles[role][account] = enabled;
        emit RoleUpdated(role, account, enabled);
    }

    function hasRole(bytes32 role, address account) external view returns (bool) {
        return roles[role][account];
    }

    function setPaused(bool value) external onlyOwner {
        paused = value;
        emit PauseUpdated(value);
    }

    function submitEvidence(
        bytes32 evidenceId,
        bytes32 payloadHash,
        bytes32 sourceHash,
        bytes32 metadataHash,
        bytes32 lcdaId,
        uint64 observedAt,
        uint256 rainfallMmX100,
        uint256 yieldLitresX100,
        MeasurementClass measurementClass
    ) external onlyRole(SUBMITTER_ROLE) whenNotPaused {
        require(evidenceId != bytes32(0), "ZERO_EVIDENCE_ID");
        require(payloadHash != bytes32(0), "ZERO_PAYLOAD_HASH");
        require(lcdaId != bytes32(0), "ZERO_LCDA_ID");
        require(observedAt != 0 && observedAt <= block.timestamp, "INVALID_OBSERVED_AT");
        require(!evidenceExists[evidenceId], "DUPLICATE_EVIDENCE");
        // Forecasts are operational inputs and must never become DMRV production evidence.
        require(measurementClass == MeasurementClass.OBSERVED, "FORECAST_NOT_DMRV");

        evidence[evidenceId] = Evidence({
            evidenceId: evidenceId,
            payloadHash: payloadHash,
            sourceHash: sourceHash,
            metadataHash: metadataHash,
            lcdaId: lcdaId,
            observedAt: observedAt,
            submittedAt: uint64(block.timestamp),
            rainfallMmX100: rainfallMmX100,
            yieldLitresX100: yieldLitresX100,
            measurementClass: measurementClass,
            state: EvidenceState.SUBMITTED,
            submitter: msg.sender,
            verifier: address(0)
        });
        evidenceExists[evidenceId] = true;
        emit EvidenceSubmitted(evidenceId, payloadHash, lcdaId, observedAt, msg.sender);
    }

    function verifyEvidence(bytes32 evidenceId) external onlyRole(VERIFIER_ROLE) whenNotPaused {
        Evidence storage item = evidence[evidenceId];
        require(evidenceExists[evidenceId], "UNKNOWN_EVIDENCE");
        require(item.state == EvidenceState.SUBMITTED, "BAD_STATE");
        item.state = EvidenceState.VERIFIED;
        item.verifier = msg.sender;
        emit EvidenceVerified(evidenceId, msg.sender, uint64(block.timestamp));
    }

    function rejectEvidence(bytes32 evidenceId) external onlyRole(VERIFIER_ROLE) whenNotPaused {
        Evidence storage item = evidence[evidenceId];
        require(evidenceExists[evidenceId], "UNKNOWN_EVIDENCE");
        require(item.state == EvidenceState.SUBMITTED, "BAD_STATE");
        item.state = EvidenceState.REJECTED;
        item.verifier = msg.sender;
        emit EvidenceRejected(evidenceId, msg.sender, uint64(block.timestamp));
    }

    function getEvidence(bytes32 evidenceId) external view returns (Evidence memory) {
        require(evidenceExists[evidenceId], "UNKNOWN_EVIDENCE");
        return evidence[evidenceId];
    }
}
