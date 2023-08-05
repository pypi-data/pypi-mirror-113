Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
var tagFilter_1 = tslib_1.__importDefault(require("app/views/issueList/tagFilter"));
describe('IssueListTagFilter', function () {
    // @ts-expect-error
    MockApiClient.clearMockResponses();
    var selectMock = jest.fn();
    var tag = { key: 'browser', name: 'Browser' };
    var tagValueLoader = function () {
        return new Promise(function (resolve) {
            return resolve([
                {
                    count: 0,
                    firstSeen: '2018-05-30T11:33:46.535Z',
                    key: 'foo',
                    lastSeen: '2018-05-30T11:33:46.535Z',
                    name: 'foo',
                    value: 'foo',
                    id: 'foo',
                    ip_address: '192.168.1.1',
                    email: 'foo@boy.cat',
                    username: 'foo',
                },
                {
                    count: 0,
                    firstSeen: '2018-05-30T11:33:46.535Z',
                    key: 'fooBaar',
                    lastSeen: '2018-05-30T11:33:46.535Z',
                    name: 'fooBaar',
                    value: 'fooBaar',
                    id: 'fooBaar',
                    ip_address: '192.168.1.1',
                    email: 'fooBaar@boy.cat',
                    username: 'ffooBaaroo',
                },
            ]);
        });
    };
    it('calls API and renders options when opened', function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, getByLabelText, getByText, getAllByText, input, loadingIndicator, allFoo, menuOptionFoo;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = reactTestingLibrary_1.mountWithTheme(<tagFilter_1.default tag={tag} value="" onSelect={selectMock} tagValueLoader={tagValueLoader}/>), getByLabelText = _a.getByLabelText, getByText = _a.getByText, getAllByText = _a.getAllByText;
                        input = getByLabelText(tag.key);
                        reactTestingLibrary_1.fireEvent.change(input, { target: { value: 'foo' } });
                        loadingIndicator = getByText('Loading\u2026');
                        return [4 /*yield*/, reactTestingLibrary_1.waitFor(function () { return expect(loadingIndicator).not.toBeInTheDocument(); })];
                    case 1:
                        _b.sent();
                        allFoo = getAllByText('foo');
                        menuOptionFoo = allFoo[1];
                        reactTestingLibrary_1.fireEvent.click(menuOptionFoo);
                        expect(selectMock).toHaveBeenCalledWith(tag, 'foo');
                        return [2 /*return*/];
                }
            });
        });
    });
});
//# sourceMappingURL=tagFilter.spec.jsx.map