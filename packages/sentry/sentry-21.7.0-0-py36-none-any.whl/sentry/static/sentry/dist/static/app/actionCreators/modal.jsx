Object.defineProperty(exports, "__esModule", { value: true });
exports.openReprocessEventModal = exports.openAddDashboardWidgetModal = exports.openInviteMembersModal = exports.openDebugFileSourceModal = exports.openHelpSearchModal = exports.redirectToProject = exports.openTeamAccessRequestModal = exports.openRecoveryOptions = exports.openCommandPalette = exports.openEditOwnershipRules = exports.openCreateOwnershipRule = exports.openCreateTeamModal = exports.openDiffModal = exports.openEmailVerification = exports.openSudo = exports.closeModal = exports.openModal = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var modalActions_1 = tslib_1.__importDefault(require("app/actions/modalActions"));
/**
 * Show a modal
 */
function openModal(renderer, options) {
    modalActions_1.default.openModal(renderer, options);
}
exports.openModal = openModal;
/**
 * Close modal
 */
function closeModal() {
    modalActions_1.default.closeModal();
}
exports.closeModal = closeModal;
function openSudo(_a) {
    if (_a === void 0) { _a = {}; }
    var onClose = _a.onClose, args = tslib_1.__rest(_a, ["onClose"]);
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/sudoModal')); })];
                case 1:
                    mod = _b.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...args}/>; }, { onClose: onClose });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openSudo = openSudo;
function openEmailVerification(_a) {
    if (_a === void 0) { _a = {}; }
    var onClose = _a.onClose, args = tslib_1.__rest(_a, ["onClose"]);
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/emailVerificationModal')); })];
                case 1:
                    mod = _b.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...args}/>; }, { onClose: onClose });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openEmailVerification = openEmailVerification;
function openDiffModal(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/diffModal')); })];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openDiffModal = openDiffModal;
function openCreateTeamModal(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/createTeamModal')); })];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openCreateTeamModal = openCreateTeamModal;
function openCreateOwnershipRule(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/createOwnershipRuleModal')); })];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openCreateOwnershipRule = openCreateOwnershipRule;
function openEditOwnershipRules(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/editOwnershipRulesModal')); })];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { backdrop: 'static', modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openEditOwnershipRules = openEditOwnershipRules;
function openCommandPalette(options) {
    if (options === void 0) { options = {}; }
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/commandPalette')); })];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openCommandPalette = openCommandPalette;
function openRecoveryOptions(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/recoveryOptionsModal')); })];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openRecoveryOptions = openRecoveryOptions;
function openTeamAccessRequestModal(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/teamAccessRequestModal')); })];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openTeamAccessRequestModal = openTeamAccessRequestModal;
function redirectToProject(newProjectSlug) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/redirectToProject')); })];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} slug={newProjectSlug}/>; }, {});
                    return [2 /*return*/];
            }
        });
    });
}
exports.redirectToProject = redirectToProject;
function openHelpSearchModal(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/helpSearchModal')); })];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openHelpSearchModal = openHelpSearchModal;
function openDebugFileSourceModal(_a) {
    var onClose = _a.onClose, restOptions = tslib_1.__rest(_a, ["onClose"]);
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require(
                    /* webpackChunkName: "DebugFileCustomRepository" */ 'app/components/modals/debugFileCustomRepository')); })];
                case 1:
                    mod = _b.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...restOptions}/>; }, {
                        modalCss: modalCss,
                        onClose: onClose,
                    });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openDebugFileSourceModal = openDebugFileSourceModal;
function openInviteMembersModal(options) {
    if (options === void 0) { options = {}; }
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/inviteMembersModal')); })];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openInviteMembersModal = openInviteMembersModal;
function openAddDashboardWidgetModal(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/addDashboardWidgetModal')); })];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { backdrop: 'static', modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openAddDashboardWidgetModal = openAddDashboardWidgetModal;
function openReprocessEventModal(_a) {
    var onClose = _a.onClose, options = tslib_1.__rest(_a, ["onClose"]);
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/modals/reprocessEventModal')); })];
                case 1:
                    mod = _b.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { onClose: onClose });
                    return [2 /*return*/];
            }
        });
    });
}
exports.openReprocessEventModal = openReprocessEventModal;
//# sourceMappingURL=modal.jsx.map