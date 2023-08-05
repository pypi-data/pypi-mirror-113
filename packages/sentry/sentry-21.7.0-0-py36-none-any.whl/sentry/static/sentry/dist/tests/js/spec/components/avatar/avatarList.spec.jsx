Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
var avatarList_1 = tslib_1.__importDefault(require("app/components/avatar/avatarList"));
function renderComponent(avatarUsersSixUsers) {
    return reactTestingLibrary_1.mountWithTheme(<avatarList_1.default users={avatarUsersSixUsers}/>);
}
describe('AvatarList', function () {
    // @ts-expect-error
    var user = TestStubs.User();
    it('renders with user letter avatars', function () {
        var users = [
            tslib_1.__assign(tslib_1.__assign({}, user), { id: '1', name: 'AB' }),
            tslib_1.__assign(tslib_1.__assign({}, user), { id: '2', name: 'BC' }),
        ];
        var _a = renderComponent(users), container = _a.container, queryByTestId = _a.queryByTestId, getByText = _a.getByText;
        expect(getByText('A')).toBeTruthy();
        expect(getByText('B')).toBeTruthy();
        expect(queryByTestId('avatarList-collapsedusers')).toBeNull();
        expect(container).toSnapshot();
    });
    it('renders with collapsed avatar count if > 5 users', function () {
        var users = [
            tslib_1.__assign(tslib_1.__assign({}, user), { id: '1', name: 'AB' }),
            tslib_1.__assign(tslib_1.__assign({}, user), { id: '2', name: 'BC' }),
            tslib_1.__assign(tslib_1.__assign({}, user), { id: '3', name: 'CD' }),
            tslib_1.__assign(tslib_1.__assign({}, user), { id: '4', name: 'DE' }),
            tslib_1.__assign(tslib_1.__assign({}, user), { id: '5', name: 'EF' }),
            tslib_1.__assign(tslib_1.__assign({}, user), { id: '6', name: 'FG' }),
        ];
        var _a = renderComponent(users), container = _a.container, getByTestId = _a.getByTestId, queryByText = _a.queryByText, queryAllByText = _a.queryAllByText;
        expect(queryAllByText(users[0].name.charAt(0))).toBeTruthy();
        expect(queryAllByText(users[1].name.charAt(0))).toBeTruthy();
        expect(queryAllByText(users[2].name.charAt(0))).toBeTruthy();
        expect(queryAllByText(users[3].name.charAt(0))).toBeTruthy();
        expect(queryAllByText(users[4].name.charAt(0))).toBeTruthy();
        expect(queryByText(users[5].name.charAt(0))).toBeNull();
        expect(getByTestId('avatarList-collapsedusers')).toBeTruthy();
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=avatarList.spec.jsx.map