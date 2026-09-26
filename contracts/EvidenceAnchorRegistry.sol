// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title EvidenceAnchorRegistry
/// @notice Minimal tamper-evidence registry for deterministic DMRV package roots.
/// @dev The contract anchors a package identifier and SHA-256 digest. It does not
///      attest to environmental truth, regulatory compliance, water quality, or ESG claims.
contract EvidenceAnchorRegistry {
    struct Anchor {
        bytes32 digest;
        uint64 anchoredAt;
        address submitter;
    }

    mapping(bytes32 => Anchor) private anchors;

    event EvidenceAnchored(
        bytes32 indexed packageId,
        bytes32 indexed digest,
        uint64 anchoredAt,
        address indexed submitter
    );

    error AlreadyAnchored(bytes32 packageId);
    error EmptyPackageId();
    error EmptyDigest();

    function anchor(bytes32 packageId, bytes32 digest) external {
        if (packageId == bytes32(0)) revert EmptyPackageId();
        if (digest == bytes32(0)) revert EmptyDigest();
        if (anchors[packageId].anchoredAt != 0) revert AlreadyAnchored(packageId);

        uint64 timestamp = uint64(block.timestamp);
        anchors[packageId] = Anchor(digest, timestamp, msg.sender);
        emit EvidenceAnchored(packageId, digest, timestamp, msg.sender);
    }

    function getAnchor(bytes32 packageId) external view returns (Anchor memory) {
        return anchors[packageId];
    }

    function verify(bytes32 packageId, bytes32 digest) external view returns (bool) {
        Anchor memory record = anchors[packageId];
        return record.anchoredAt != 0 && record.digest == digest;
    }
}
