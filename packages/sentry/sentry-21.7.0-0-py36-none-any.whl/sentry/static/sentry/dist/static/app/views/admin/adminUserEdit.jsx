Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var radioGroup_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/radioGroup"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var model_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/model"));
var userEditForm = {
    title: 'User details',
    fields: [
        {
            name: 'name',
            type: 'string',
            required: true,
            label: locale_1.t('Name'),
        },
        {
            name: 'username',
            type: 'string',
            required: true,
            label: locale_1.t('Username'),
            help: locale_1.t('The username is the unique id of the user in the system'),
        },
        {
            name: 'email',
            type: 'string',
            required: true,
            label: locale_1.t('Email'),
            help: locale_1.t('The users primary email address'),
        },
        {
            name: 'isActive',
            type: 'boolean',
            required: true,
            label: locale_1.t('Active'),
            help: locale_1.t('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),
        },
        {
            name: 'isStaff',
            type: 'boolean',
            required: true,
            label: locale_1.t('Admin'),
            help: locale_1.t('Designates whether this user can perform administrative functions.'),
        },
        {
            name: 'isSuperuser',
            type: 'boolean',
            required: true,
            label: locale_1.t('Superuser'),
            help: locale_1.t('Designates whether this user has all permissions without explicitly assigning them.'),
        },
    ],
};
var REMOVE_BUTTON_LABEL = {
    disable: locale_1.t('Disable User'),
    delete: locale_1.t('Permanently Delete User'),
};
var RemoveUserModal = /** @class */ (function (_super) {
    tslib_1.__extends(RemoveUserModal, _super);
    function RemoveUserModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            deleteType: 'disable',
        };
        _this.onRemove = function () {
            _this.props.onRemove(_this.state.deleteType);
            _this.props.closeModal();
        };
        return _this;
    }
    RemoveUserModal.prototype.render = function () {
        var _this = this;
        var user = this.props.user;
        var deleteType = this.state.deleteType;
        return (<react_1.Fragment>
        <radioGroup_1.default value={deleteType} label={locale_1.t('Remove user %s', user.email)} onChange={function (type) { return _this.setState({ deleteType: type }); }} choices={[
                ['disable', locale_1.t('Disable the account.')],
                ['delete', locale_1.t('Permanently remove the user and their data.')],
            ]}/>
        <ModalFooter>
          <button_1.default priority="danger" onClick={this.onRemove}>
            {REMOVE_BUTTON_LABEL[deleteType]}
          </button_1.default>
          <button_1.default onClick={this.props.closeModal}>{locale_1.t('Cancel')}</button_1.default>
        </ModalFooter>
      </react_1.Fragment>);
    };
    return RemoveUserModal;
}(react_1.Component));
var AdminUserEdit = /** @class */ (function (_super) {
    tslib_1.__extends(AdminUserEdit, _super);
    function AdminUserEdit() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.removeUser = function (actionTypes) {
            return actionTypes === 'delete' ? _this.deleteUser() : _this.deactivateUser();
        };
        _this.formModel = new model_1.default();
        return _this;
    }
    Object.defineProperty(AdminUserEdit.prototype, "userEndpoint", {
        get: function () {
            var params = this.props.params;
            return "/users/" + params.id + "/";
        },
        enumerable: false,
        configurable: true
    });
    AdminUserEdit.prototype.getEndpoints = function () {
        return [['user', this.userEndpoint]];
    };
    AdminUserEdit.prototype.deleteUser = function () {
        var _a;
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0: return [4 /*yield*/, this.api.requestPromise(this.userEndpoint, {
                            method: 'DELETE',
                            data: { hardDelete: true, organizations: [] },
                        })];
                    case 1:
                        _b.sent();
                        indicator_1.addSuccessMessage(locale_1.t("%s's account has been deleted.", (_a = this.state.user) === null || _a === void 0 ? void 0 : _a.email));
                        react_router_1.browserHistory.replace('/manage/users/');
                        return [2 /*return*/];
                }
            });
        });
    };
    AdminUserEdit.prototype.deactivateUser = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var response;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.api.requestPromise(this.userEndpoint, {
                            method: 'PUT',
                            data: { isActive: false },
                        })];
                    case 1:
                        response = _a.sent();
                        this.setState({ user: response });
                        this.formModel.setInitialData(response);
                        indicator_1.addSuccessMessage(locale_1.t("%s's account has been deactivated.", response.email));
                        return [2 /*return*/];
                }
            });
        });
    };
    AdminUserEdit.prototype.renderBody = function () {
        var _this = this;
        var user = this.state.user;
        if (user === null) {
            return null;
        }
        var openDeleteModal = function () {
            return modal_1.openModal(function (opts) { return (<RemoveUserModal user={user} onRemove={_this.removeUser} {...opts}/>); });
        };
        return (<react_1.Fragment>
        <h3>{locale_1.t('Users')}</h3>
        <p>{locale_1.t('Editing user: %s', user.email)}</p>
        <form_1.default model={this.formModel} initialData={user} apiMethod="PUT" apiEndpoint={this.userEndpoint} requireChanges onSubmitError={indicator_1.addErrorMessage} onSubmitSuccess={function (data) {
                _this.setState({ user: data });
                indicator_1.addSuccessMessage('User account updated.');
            }} extraButton={<button_1.default type="button" onClick={openDeleteModal} style={{ marginLeft: space_1.default(1) }} priority="danger">
              {locale_1.t('Remove User')}
            </button_1.default>}>
          <jsonForm_1.default forms={[userEditForm]}/>
        </form_1.default>
      </react_1.Fragment>);
    };
    return AdminUserEdit;
}(asyncView_1.default));
var ModalFooter = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: end;\n  padding: 20px 30px;\n  margin: 20px -30px -30px;\n  border-top: 1px solid ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: end;\n  padding: 20px 30px;\n  margin: 20px -30px -30px;\n  border-top: 1px solid ", ";\n"])), space_1.default(1), function (p) { return p.theme.border; });
exports.default = AdminUserEdit;
var templateObject_1;
//# sourceMappingURL=adminUserEdit.jsx.map