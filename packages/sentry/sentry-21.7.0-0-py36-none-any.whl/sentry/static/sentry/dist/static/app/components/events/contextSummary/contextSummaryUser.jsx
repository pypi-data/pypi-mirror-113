Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var utils_1 = require("app/components/events/interfaces/utils");
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var contextSummaryNoSummary_1 = tslib_1.__importDefault(require("./contextSummaryNoSummary"));
var item_1 = tslib_1.__importDefault(require("./item"));
var ContextSummaryUser = function (_a) {
    var data = _a.data;
    var user = utils_1.removeFilterMaskedEntries(data);
    if (Object.keys(user).length === 0) {
        return <contextSummaryNoSummary_1.default title={locale_1.t('Unknown User')}/>;
    }
    var renderUserDetails = function (key) {
        var userDetails = {
            subject: locale_1.t('Username:'),
            value: user.username,
            meta: metaProxy_1.getMeta(data, 'username'),
        };
        if (key === 'id') {
            userDetails.subject = locale_1.t('ID:');
            userDetails.value = user.id;
            userDetails.meta = metaProxy_1.getMeta(data, 'id');
        }
        return (<textOverflow_1.default isParagraph>
        <Subject>{userDetails.subject}</Subject>
        <annotatedText_1.default value={userDetails.value} meta={userDetails.meta}/>
      </textOverflow_1.default>);
    };
    var getUserTitle = function () {
        if (user.email) {
            return {
                value: user.email,
                meta: metaProxy_1.getMeta(data, 'email'),
            };
        }
        if (user.ip_address) {
            return {
                value: user.ip_address,
                meta: metaProxy_1.getMeta(data, 'ip_address'),
            };
        }
        if (user.id) {
            return {
                value: user.id,
                meta: metaProxy_1.getMeta(data, 'id'),
            };
        }
        if (user.username) {
            return {
                value: user.username,
                meta: metaProxy_1.getMeta(data, 'username'),
            };
        }
        return undefined;
    };
    var userTitle = getUserTitle();
    if (!userTitle) {
        return <contextSummaryNoSummary_1.default title={locale_1.t('Unknown User')}/>;
    }
    var icon = userTitle ? (<userAvatar_1.default user={user} size={32} className="context-item-icon" gravatar={false}/>) : (<span className="context-item-icon"/>);
    return (<item_1.default className="user" icon={icon}>
      {userTitle && (<h3 data-test-id="user-title">
          <annotatedText_1.default value={userTitle.value} meta={userTitle.meta}/>
        </h3>)}
      {user.id && user.id !== (userTitle === null || userTitle === void 0 ? void 0 : userTitle.value)
            ? renderUserDetails('id')
            : user.username &&
                user.username !== (userTitle === null || userTitle === void 0 ? void 0 : userTitle.value) &&
                renderUserDetails('username')}
    </item_1.default>);
};
exports.default = ContextSummaryUser;
var Subject = styled_1.default('strong')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.5));
var templateObject_1;
//# sourceMappingURL=contextSummaryUser.jsx.map