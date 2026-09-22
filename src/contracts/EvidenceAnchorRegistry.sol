// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title OMI-OJO Evidence Anchor Registry
/// @notice Stores deterministic evidence roots for auditability.
/// @dev An anchor proves that a root was committed at a given block. It does
///      not prove the truth, quality, legality, or sustainability of the data.
contract EvidenceAnchorRegistry {
    struct Anchor {
        bytes32 root;
        uint64 anchoredAt;
        address submitter;
        uint256 chainId;
    }

    mapping(bytes32 => Anchor) private _anchors;

    event EvidenceAnchored(
        bytes32 indexed evidenceId,
        bytes32 indexed evidenceRoot,
        address indexed submitter,
        uint256 chainId,
        uint256 blockNumber,
        uint256 blockTimestamp
    );

    event EvidenceSuperseded(
        bytes32 indexed evidenceId,
        bytes32 indexed previousRoot,
        bytes32 indexed successorRoot,
        address submitter
    );

    error InvalidEvidenceId();
    error InvalidRoot();
    error AlreadyAnchored();
    error UnknownEvidence();
    error SameRoot();
    error Unauthorized();

    address public immutable anchorAdmin;

    constructor(address admin) {
        if (admin == address(0)) revert Unauthorized();
        anchorAdmin = admin;
    }

    function anchor(bytes32 evidenceId, bytes32 evidenceRoot) external {
        if (evidenceId == bytes32(0)) revert InvalidEvidenceId();
        if (evidenceRoot == bytes32(0)) revert InvalidRoot();

        Anchor storage existing = _anchors[evidenceId];
        if (existing.root != bytes32(0)) revert AlreadyAnchored();

        _anchors[evidenceId] = Anchor({
            root: evidenceRoot,
            anchoredAt: uint64(block.timestamp),
            submitter: msg.sender,
            chainId: block.chainid
        });

        emit EvidenceAnchored(
            evidenceId,
            evidenceRoot,
            msg.sender,
            block.chainid,
            block.number,
            block.timestamp
        );
    }

    /// @notice Creates an append-only successor after a correction.
    /// @dev The old root remains immutable and discoverable.
    function supersede(
        bytes32 evidenceId,
        bytes32 successorEvidenceId,
        bytes32 successorRoot
    ) external {
        if (msg.sender != anchorAdmin) revert Unauthorized();
        if (evidenceId == bytes32(0) || successorEvidenceId == bytes32(0)) {
            revert InvalidEvidenceId();
        }
        if (successorRoot == bytes32(0)) revert InvalidRoot();

        Anchor memory previous = _anchors[evidenceId];
        if (previous.root == bytes32(0)) revert UnknownEvidence();
        if (_anchors[successorEvidenceId].root != bytes32(0)) revert AlreadyAnchored();
        if (previous.root == successorRoot) revert SameRoot();

        _anchors[successorEvidenceId] = Anchor({
            root: successorRoot,
            anchoredAt: uint64(block.timestamp),
            submitter: msg.sender,
            chainId: block.chainid
        });

        emit EvidenceSuperseded(evidenceId, previous.root, successorRoot, msg.sender);
        emit EvidenceAnchored(
            successorEvidenceId,
            successorRoot,
            msg.sender,
            block.chainid,
            block.number,
            block.timestamp
        );
    }

    function getAnchor(bytes32 evidenceId) external view returns (Anchor memory) {
        return _anchors[evidenceId];
    }

    function isAnchored(bytes32 evidenceId, bytes32 expectedRoot) external view returns (bool) {
        Anchor memory a = _anchors[evidenceId];
        return a.root != bytes32(0) && a.root == expectedRoot;
    }
}
