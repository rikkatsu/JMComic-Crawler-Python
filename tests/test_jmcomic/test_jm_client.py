from test_jmcomic import *


class Test_Client(JmTestConfigurable):

    def test_download_image(self):
        jm_photo_id = 'JM438516'
        photo = self.client.get_photo_detail(jm_photo_id)
        image = photo[0]
        filepath = self.option.decide_image_filepath(image)
        self.client.download_by_image_detail(image, filepath)
        print(filepath)

    def test_fetch_album(self):
        album_id = "JM438516"
        self.client.get_album_detail(album_id)

    def test_search(self):
        page: JmSearchPage = self.client.search_tag('+无修正 +中文 -全彩')

        if len(page) >= 1:
            for aid, ainfo in page[0:1:1]:
                print(aid, ainfo)

        for aid, atitle, tag_list in page.iter_id_title_tag():
            print(aid, atitle, tag_list)

        aid = '438516'
        page = self.client.search_site(aid)
        search_aid, ainfo = page[0]
        self.assertEqual(search_aid, aid)

    def test_gt_300_photo(self):
        photo_id = '147643'
        photo: JmPhotoDetail = self.client.get_photo_detail(photo_id)
        image = photo[3000]
        print(image.img_url)
        self.client.download_by_image_detail(image, self.option.decide_image_filepath(image))

    def test_album_missing(self):
        class A(BaseException):
            pass

        JmModuleConfig.CLASS_EXCEPTION = A
        self.assertRaises(
            A,
            self.client.get_album_detail,
            '0'
        )

    def test_raise_exception(self):

        class B(BaseException):
            pass

        def raises(old, _msg, _extra):
            self.assertEqual(old, default_raise_exception_executor)
            raise B()

        JmModuleConfig.raise_exception_executor = default_raise_exception_executor
        ExceptionTool.replace_old_exception_executor(raises)
        self.assertRaises(B, JmcomicText.parse_to_jm_id, 'asdhasjhkd')
        # 还原
        JmModuleConfig.raise_exception_executor = default_raise_exception_executor

    def test_detail_property_list(self):
        album = self.client.get_album_detail(410090)

        ans = [
            (album.works, ['原神', 'Genshin']),
            (album.actors, ['申鶴', '神里綾華', '甘雨']),
            (album.tags, ['C101', '巨乳', '校服', '口交', '乳交', '群交', '連褲襪', '中文', '禁漫漢化組', '纯爱']),
            (album.authors, ['うぱ西']),
        ]

        for pair in ans:
            self.assertListEqual(pair[0][0:9], pair[1][0:9])

    def test_photo_sort(self):
        client = self.option.build_jm_client()

        # 测试用例 - 单章本子
        single_photo_album_is = str_to_list('''
        430371
        438696
        432888
        ''')

        # 测试用例 - 多章本子
        multi_photo_album_is = str_to_list('''
        400222
        122061
        ''')

        photo_dict: Dict[str, JmPhotoDetail] = multi_call(client.get_photo_detail, single_photo_album_is)
        album_dict: Dict[str, JmAlbumDetail] = multi_call(client.get_album_detail, single_photo_album_is)

        for each in photo_dict.values():
            each: JmPhotoDetail
            self.assertEqual(each.album_index, 1)

        for each in album_dict.values():
            each: JmAlbumDetail
            self.assertEqual(each[0].album_index, 1)

        print_eye_catching('【通过】测试用例 - 单章本子')
        multi_photo_album_dict: Dict[JmAlbumDetail, List[JmPhotoDetail]] = {}

        def run(aid):
            album = client.get_album_detail(aid)

            photo_dict = multi_call(
                client.get_photo_detail,
                (photo.photo_id for photo in album),
                launcher=thread_pool_executor,
            )

            multi_photo_album_dict[album] = list(photo_dict.values())

        multi_thread_launcher(
            iter_objs=multi_photo_album_is,
            apply_each_obj_func=run,
        )

        for album, photo_ls in multi_photo_album_dict.items():
            ls1 = sorted([each.sort for each in album])
            ls2 = sorted([ans.sort for ans in photo_ls])
            print(ls1)
            print(ls2)
            self.assertListEqual(
                ls1,
                ls2,
                album.album_id
            )

    def test_getitem_and_slice(self):
        cl: JmcomicClient = self.client
        cases = [
            ['400222', 0, [400222]],
            ['400222', 1, [413446]],
            ['400222', (None, 1), [400222]],
            ['400222', (1, 3), [413446, 413447]],
            ['413447', (1, 3), [2, 3], []],
        ]

        for [jmid, slicearg, *args] in cases:
            ans = args[0]

            if len(args) == 1:
                func = cl.get_album_detail
            else:
                func = cl.get_photo_detail

            jmentity = func(jmid)

            ls: List[Union[JmPhotoDetail, JmImageDetail]]
            if isinstance(slicearg, int):
                ls = [jmentity[slicearg]]
            elif len(slicearg) == 2:
                ls = jmentity[slicearg[0]: slicearg[1]]
            else:
                ls = jmentity[slicearg[0]: slicearg[1]: slicearg[2]]

            if len(args) == 1:
                self.assertListEqual(
                    list1=[int(e.id) for e in ls],
                    list2=ans,
                )
            else:
                self.assertListEqual(
                    list1=[int(e.img_file_name) for e in ls],
                    list2=ans,
                )

    def test_search_advanced(self):
        elist = []

        def search_and_test(expected_result, params):
            try:
                page = self.client.search_site(**params)
                print(page)
                assert int(page[0][0]) == expected_result
            except Exception as e:
                elist.append(e)

        # 定义测试用例
        cases = {
            152637: {
                'search_query': '无修正',
                'order_by': JmSearchAlbumClient.ORDER_BY_LIKE,
                'time': JmSearchAlbumClient.TIME_ALL,
            },
            147643: {
                'search_query': '无修正',
                'order_by': JmSearchAlbumClient.ORDER_BY_PICTURE,
                'time': JmSearchAlbumClient.TIME_ALL,
            },
        }

        multi_thread_launcher(
            iter_objs=cases.items(),
            apply_each_obj_func=search_and_test,
        )

        if len(elist) == 0:
            return

        for e in elist:
            print(e)

        raise AssertionError(elist)

    def test_comment_count(self):
        aid = 'JM438516'
        album = self.client.get_album_detail(aid)
        self.assertGreater(album.comment_count, 0)
        page = self.client.search_site('无修正')
        for i in range(3):
            aid, _atitle = page[i]
            self.assertGreaterEqual(
                self.client.get_album_detail(aid).comment_count,
                0,
                aid,
            )

    def test_get_detail(self):
        client = self.client

        album = client.get_album_detail(400222)
        print(album.id, album.name, album.tags)

        for photo in album[0:3]:
            photo = client.get_photo_detail(photo.photo_id)
            print(photo.id, photo.name)

    def test_cache_result_equal(self):
        cl = self.client
        cases = [
            (123, False, False),
            (123,),
            (123, False, True),
            (123, True, False),
        ]

        ans = None
        for args in cases:
            photo = cl.get_photo_detail(*args)
            if ans is None:
                ans = id(photo)
            else:
                self.assertEqual(ans, id(photo))
