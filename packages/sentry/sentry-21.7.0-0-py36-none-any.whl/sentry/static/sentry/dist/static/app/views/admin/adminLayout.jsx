Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var settingsLayout_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsLayout"));
var settingsNavigation_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsNavigation"));
var AdminNavigation = function () { return (<settingsNavigation_1.default stickyTop="0" navigationObjects={[
        {
            name: 'System Status',
            items: [
                { path: '/manage/', index: true, title: 'Overview' },
                { path: '/manage/buffer/', title: 'Buffer' },
                { path: '/manage/queue/', title: 'Queue' },
                { path: '/manage/quotas/', title: 'Quotas' },
                { path: '/manage/status/environment/', title: 'Environment' },
                { path: '/manage/status/packages/', title: 'Packages' },
                { path: '/manage/status/mail/', title: 'Mail' },
                { path: '/manage/status/warnings/', title: 'Warnings' },
                { path: '/manage/settings/', title: 'Settings' },
            ],
        },
        {
            name: 'Manage',
            items: [
                { path: '/manage/organizations/', title: 'Organizations' },
                { path: '/manage/projects/', title: 'Projects' },
                { path: '/manage/users/', title: 'Users' },
            ],
        },
    ]}/>); };
function AdminLayout(_a) {
    var children = _a.children, props = tslib_1.__rest(_a, ["children"]);
    return (<react_document_title_1.default title="Sentry Admin">
      <Page>
        <settingsLayout_1.default renderNavigation={AdminNavigation} {...props}>
          {children}
        </settingsLayout_1.default>
      </Page>
    </react_document_title_1.default>);
}
exports.default = AdminLayout;
var Page = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-grow: 1;\n  margin-bottom: -20px;\n"], ["\n  display: flex;\n  flex-grow: 1;\n  margin-bottom: -20px;\n"])));
var templateObject_1;
//# sourceMappingURL=adminLayout.jsx.map